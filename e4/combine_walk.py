import os
import pathlib
import sys
import numpy as np
import pandas as pd
from xml.dom.minidom import getDOMImplementation
import gzip
import json
import xml.etree.ElementTree as ET

def output_gpx(points, output_filename):
    """
    Output a GPX file with latitude and longitude from the points DataFrame.
    """
    xmlns = 'http://www.topografix.com/GPX/1/0'
    def append_trkpt(pt, trkseg, doc):
        trkpt = doc.createElement('trkpt')
        trkpt.setAttribute('lat', '%.10f' % (pt['lat']))
        trkpt.setAttribute('lon', '%.10f' % (pt['lon']))
        time = doc.createElement('time')
        time.appendChild(doc.createTextNode(pt['datetime'].strftime("%Y-%m-%dT%H:%M:%SZ")))
        trkpt.appendChild(time)
        trkseg.appendChild(trkpt)
    doc = getDOMImplementation().createDocument(None, 'gpx', None)
    trk = doc.createElement('trk')
    doc.documentElement.appendChild(trk)
    trkseg = doc.createElement('trkseg')
    trk.appendChild(trkseg)
    points.apply(append_trkpt, axis=1, trkseg=trkseg, doc=doc)
    doc.documentElement.setAttribute('xmlns', xmlns)
    with open(output_filename, 'w') as fh:
        fh.write(doc.toprettyxml(indent='  '))

def get_gps_data(gpx_path):
    tree = ET.parse(gpx_path)
    root = tree.getroot()
    ns = {'default': 'http://www.topografix.com/GPX/1/0'}
    points = []
    for trkpt in root.findall('.//default:trkpt', ns):
        lat = float(trkpt.attrib['lat'])
        lon = float(trkpt.attrib['lon'])
        time = trkpt.find('default:time', ns).text
        points.append({'datetime': pd.to_datetime(time), 'lat': lat, 'lon': lon})
    return pd.DataFrame(points)

def main():
    input_directory = pathlib.Path(sys.argv[1])
    output_directory = pathlib.Path(sys.argv[2])
    # Read GoPro accl data
    with gzip.open(input_directory / 'accl.ndjson.gz', 'rt') as f:
        accl = pd.DataFrame([json.loads(line) for line in f])
    accl['timestamp'] = pd.to_datetime(accl['timestamp'])
    accl = accl[['timestamp', 'x']]
    # Read GoPro GPS data
    gps = get_gps_data(input_directory / 'gopro.gpx')
    # Read phone data
    phone = pd.read_csv(input_directory / 'phone.csv.gz')[['time', 'gFx', 'Bx', 'By']]
    # Align phone timestamps to GoPro accl start
    first_time = accl['timestamp'].min()
    best_offset = 0
    best_corr = -np.inf
    # Bin size in seconds
    BIN = 4
    # Pre-bin accl
    accl['bin'] = (accl['timestamp'].astype('int64') // 10**9 // BIN) * BIN
    accl_binned = accl.groupby('bin').mean(numeric_only=True)
    for offset in np.linspace(-5.0, 5.0, 101):
        phone['timestamp'] = first_time + pd.to_timedelta(phone['time'] + offset, unit='sec')
        phone['bin'] = (phone['timestamp'].astype('int64') // 10**9 // BIN) * BIN
        phone_binned = phone.groupby('bin').mean(numeric_only=True)
        merged = pd.merge(accl_binned, phone_binned, left_index=True, right_index=True, how='inner')
        if len(merged) == 0:
            continue
        corr = (merged['x'] * merged['gFx']).sum()
        if corr > best_corr:
            best_corr = corr
            best_offset = offset
    # Final phone binning with best offset
    phone['timestamp'] = first_time + pd.to_timedelta(phone['time'] + best_offset, unit='sec')
    phone['bin'] = (phone['timestamp'].astype('int64') // 10**9 // BIN) * BIN
    phone_binned = phone.groupby('bin').mean(numeric_only=True)
    # Final accl binning
    accl['bin'] = (accl['timestamp'].astype('int64') // 10**9 // BIN) * BIN
    accl_binned = accl.groupby('bin').mean(numeric_only=True)
    # Bin GPS
    gps['bin'] = (gps['datetime'].astype('int64') // 10**9 // BIN) * BIN
    gps_binned = gps.groupby('bin').first()
    # Merge all
    combined = pd.merge(accl_binned, phone_binned, left_index=True, right_index=True, how='inner')
    combined = pd.merge(combined, gps_binned, left_index=True, right_index=True, how='inner')
    combined['datetime'] = pd.to_datetime(combined.index, unit='s')
    print(f'Best time offset: {best_offset:.1f}')
    os.makedirs(output_directory, exist_ok=True)
    output_gpx(combined[['datetime', 'lat', 'lon']], output_directory / 'walk.gpx')
    combined[['datetime', 'Bx', 'By']].to_csv(output_directory / 'walk.csv', index=False)

if __name__ == '__main__':
    main()
