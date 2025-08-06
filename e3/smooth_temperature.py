import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.nonparametric.smoothers_lowess import lowess
from pykalman import KalmanFilter

def smooth_temperature(file_path):
    # Load the data from the CSV file
    cpu_data = pd.read_csv(file_path)
    
    # Convert timestamp to datetime and then to seconds since start
    cpu_data['timestamp'] = pd.to_datetime(cpu_data['timestamp'])
    cpu_data['time_seconds'] = (cpu_data['timestamp'] - cpu_data['timestamp'].iloc[0]).dt.total_seconds()

    # Plot the original temperature data
    plt.figure(figsize=(12, 4))
    plt.plot(cpu_data['time_seconds'], cpu_data['temperature'], 'b.', alpha=0.5)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Temperature (°C)')
    plt.title('Raw CPU Temperature Data')

    # LOESS smoothing
    loess_smoothed = lowess(cpu_data['temperature'], cpu_data['time_seconds'], frac=0.01)
    plt.plot(cpu_data['time_seconds'], loess_smoothed[:, 1], 'r-', label='LOESS Smoothed')
    
    # Kalman smoothing
    kalman_data = cpu_data[['temperature', 'cpu_percent', 'sys_load_1', 'fan_rpm']]
    initial_state = kalman_data.iloc[0].to_numpy() 
    observation_covariance = np.diag([2, 2, 2, 2]) ** 2
    transition_covariance = np.diag([0.05, 0.05, 0.05, 0.05]) ** 2
    transition = [[0.97, 0.5, 0.2, -0.001], [0.1, 0.4, 2.1, 0], [0, 0, 0.94, 0], [0, 0, 0, 1]]
    kf = KalmanFilter(initial_state_mean=initial_state,
                      observation_covariance=observation_covariance,
                      transition_covariance=transition_covariance,
                      transition_matrices=transition)
    kalman_smoothed, _ = kf.smooth(kalman_data)
    plt.plot(cpu_data['time_seconds'], kalman_smoothed[:, 0], 'g-', label='Kalman Smoothed')
    
    # Save the plot
    plt.legend()
    plt.savefig('cpu.svg')


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 smooth_temperature.py <csv_file_path>")
    else:
        smooth_temperature(sys.argv[1])

