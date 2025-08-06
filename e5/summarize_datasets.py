import pandas as pd
import numpy as np
import os

def describe_data(file_path):
    df = pd.read_csv(file_path)
    x = df['x']
    y = df['y']
    stats = {
        'mean_x': x.mean(),
        'std_x': x.std(),
        'min_x': x.min(),
        'max_x': x.max(),
        'mean_y': y.mean(),
        'std_y': y.std(),
        'min_y': y.min(),
        'max_y': y.max(),
        'corr': x.corr(y)
    }
    return stats

def describe_sentence(file_path, stats):
    # Simple heuristic for description
    if abs(stats['corr']) > 0.95:
        trend = 'strong linear relationship'
    elif abs(stats['corr']) > 0.7:
        trend = 'moderate linear relationship'
    elif abs(stats['corr']) > 0.3:
        trend = 'weak linear relationship'
    else:
        trend = 'little to no linear relationship'
    return f"This data set ('{os.path.basename(file_path)}') contains paired x and y values with a {trend} (r = {stats['corr']:.3f})."

files = [f"data-{i}.csv" for i in range(1,7)]
with open("summary.txt", "w") as out:
    for fname in files:
        stats = describe_data(fname)
        out.write(f"{fname}:\n")
        out.write(f"  x: mean={stats['mean_x']:.3f}, std={stats['std_x']:.3f}, min={stats['min_x']:.3f}, max={stats['max_x']:.3f}\n")
        out.write(f"  y: mean={stats['mean_y']:.3f}, std={stats['std_y']:.3f}, min={stats['min_y']:.3f}, max={stats['max_y']:.3f}\n")
        out.write(f"  correlation r = {stats['corr']:.3f}\n")
        out.write(f"  {describe_sentence(fname, stats)}\n\n")
