import matplotlib.pyplot as plt
import numpy as np

# Define the bit stream
bit_stream = "0100110001"

# Manchester encoding: 0 -> low-to-high, 1 -> high-to-low
time = []
signal = []

for i, bit in enumerate(bit_stream):
    t = i * 2
    if bit == '0':
        # Low to high
        time.extend([t,   t+1, t+1, t+2])
        signal.extend([0,   0,   1,   1])
    else:
        # High to low
        time.extend([t,   t+1, t+1, t+2])
        signal.extend([1,   1,   0,   0])

# Plotting the signal
plt.figure(figsize=(12, 3))
plt.step(time, signal, where='post')
plt.ylim(-0.5, 1.5)
plt.yticks([0, 1])
# Set x-ticks at the center of each bit interval
bit_centers = np.arange(1, len(bit_stream)*2, 2)
plt.xticks(bit_centers, list(bit_stream))
plt.xlabel('Bit Position')
plt.ylabel('Signal Level')
plt.title('Manchester Encoding of Bit Stream: ' + bit_stream)
plt.grid(True)
plt.show()