import sys
import gzip
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def haversine(lat1, lon1, lat2, lon2):
    # Vectorized haversine distance (km)
    R = 6371.0
    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)
    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c

def best_tmax(city, stations):
    dists = haversine(city['latitude'], city['longitude'], stations['latitude'], stations['longitude'])
    idx = dists.idxmin()
    return stations.loc[idx, 'avg_tmax'] / 10.0

def main():
    stations_file, city_file, output_svg = sys.argv[1:4]
    stations = pd.read_json(stations_file, lines=True)
    cities = pd.read_csv(city_file)
    # Clean city data
    cities = cities.dropna(subset=['population', 'area', 'latitude', 'longitude'])
    cities = cities.copy()
    cities['area_km2'] = cities['area'] / 1e6
    cities = cities[cities['area_km2'] <= 10000]
    cities['density'] = cities['population'] / cities['area_km2']
    # Remove cities with zero or negative density
    cities = cities[cities['density'] > 0]
    # Find best tmax for each city
    cities['avg_tmax'] = cities.apply(best_tmax, axis=1, stations=stations)
    # Plot
    plt.figure(figsize=(8,6))
    plt.scatter(cities['density'], cities['avg_tmax'], alpha=0.6)
    plt.xlabel('Population Density (people/km²)')
    plt.ylabel('Avg Max Temperature (°C)')
    plt.title('City Population Density vs. Avg Max Temperature')
    plt.tight_layout()
    plt.savefig(output_svg)

if __name__ == '__main__':
    main()
