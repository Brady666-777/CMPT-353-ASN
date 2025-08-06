import time
import pandas as pd
import numpy as np
from implementations import all_implementations

def main():
    np.random.seed(0)
    n = 1000  # number of samples per implementation
    size = 1000  # size of arrays
    data = []

    for sort in all_implementations:
        for i in range(n):
            arr = np.random.randint(0, size, size)
            start = time.time()
            _ = sort(arr)
            end = time.time()
            data.append({
                'implementation': sort.__name__,
                'time': end - start
            })

    df = pd.DataFrame(data)
    df.to_csv('data.csv', index=False)

if __name__ == '__main__':
    main()
