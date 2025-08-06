# calc_distance.py
import sys
import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
from pykalman import KalmanFilter

def get_data(gpx_file):
    """
    Parse GPX file and return DataFrame with columns: datetime, lat, lon
    """
    ns = '{http://www.topografix.com/GPX/1/0}'
    tree = ET.parse(gpx_file)
    root = tree.getroot()
    data = []
    for trkpt in root.iter(ns + 'trkpt'):
        lat = float(trkpt.attrib['lat'])
        lon = float(trkpt.attrib['lon'])
        time = trkpt.find(ns + 'time').text
        data.append({'datetime': time, 'lat': lat, 'lon': lon})
    df = pd.DataFrame(data)
    df['datetime'] = pd.to_datetime(df['datetime'], utc=True)
    return df

def haversine(lat1, lon1, lat2, lon2):
    # Earth radius in meters
    R = 6371000
    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2)
    dphi = np.radians(lat2 - lat1)
    dlambda = np.radians(lon2 - lon1)
    a = np.sin(dphi/2)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(dlambda/2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c

def distance(df):
    lat1 = df['lat'].values[:-1]
    lon1 = df['lon'].values[:-1]
    lat2 = df['lat'].values[1:]
    lon2 = df['lon'].values[1:]
    dists = haversine(lat1, lon1, lat2, lon2)
    return dists.sum()

def smooth(points):
    # Kalman filter for [lat, lon, Bx, By]
    obs = points[['lat', 'lon', 'Bx', 'By']].values
    n = obs.shape[0]
    # Transition matrix from assignment
    transition_matrix = np.eye(4)
    transition_matrix[0,2] = 5e-7
    transition_matrix[0,3] = 34e-7
    transition_matrix[1,2] = -49e-7
    transition_matrix[1,3] = 9e-7
    # Covariances
    observation_covariance = np.diag([2, 2, 2, 2])
    transition_covariance = np.diag([0.05, 0.05, 0.05, 0.05])
    initial_state_mean = obs[0]
    initial_state_covariance = np.eye(4) * 1e-8
    kf = KalmanFilter(
        transition_matrices=transition_matrix,
        observation_matrices=np.eye(4),
        transition_covariance=transition_covariance,
        observation_covariance=observation_covariance,
        initial_state_mean=initial_state_mean,
        initial_state_covariance=initial_state_covariance
    )
    smoothed, _ = kf.smooth(obs)
    result = points.copy()
    result['lat'] = smoothed[:,0]
    result['lon'] = smoothed[:,1]
    return result

def output_gpx(points, output_filename):
    from xml.dom.minidom import getDOMImplementation
    def append_trkpt(pt, trkseg, doc):
        trkpt = doc.createElement('trkpt')
        trkpt.setAttribute('lat', '%.7f' % (pt['lat']))
        trkpt.setAttribute('lon', '%.7f' % (pt['lon']))
        trkseg.appendChild(trkpt)
    doc = getDOMImplementation().createDocument(None, 'gpx', None)
    trk = doc.createElement('trk')
    doc.documentElement.appendChild(trk)
    trkseg = doc.createElement('trkseg')
    trk.appendChild(trkseg)
    points.apply(append_trkpt, axis=1, trkseg=trkseg, doc=doc)
    with open(output_filename, 'w') as fh:
        doc.writexml(fh, indent=' ')

def main():
    input_gpx = sys.argv[1]
    input_csv = sys.argv[2]
    points = get_data(input_gpx).set_index('datetime')
    sensor_data = pd.read_csv(input_csv, parse_dates=['datetime']).set_index('datetime')
    points['Bx'] = sensor_data['Bx']
    points['By'] = sensor_data['By']
    dist = distance(points)
    print(f'Unfiltered distance: {dist:.2f}')
    smoothed_points = smooth(points)
    smoothed_dist = distance(smoothed_points)
    print(f'Filtered distance: {smoothed_dist:.2f}')
    output_gpx(smoothed_points, 'out.gpx')

if __name__ == '__main__':
    main()
