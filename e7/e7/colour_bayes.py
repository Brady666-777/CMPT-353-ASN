import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from skimage.color import rgb2lab
from colour_bayes_hint import plot_predictions


def rgb_to_lab_transform(X):
    """Convert RGB values to LAB color space."""
    # Reshape for skimage (needs 3D array)
    X_reshaped = X.reshape(-1, 1, 3)
    # Convert to LAB
    X_lab = rgb2lab(X_reshaped)
    # Reshape back to 2D
    return X_lab.reshape(-1, 3)


def main(infile):
    # Read data
    data = pd.read_csv(infile)
    # Extract RGB features and normalize to 0-1
    X = data[['R', 'G', 'B']].values / 255.0
    # Extract labels
    y = data['Label'].values

    # Split into training and validation sets
    X_train, X_val, y_train, y_val = train_test_split(X, y, random_state=0)

    # Build model_rgb to predict y from RGB values
    model_rgb = GaussianNB()
    model_rgb.fit(X_train, y_train)
    
    # Print model_rgb's accuracy score
    rgb_accuracy = model_rgb.score(X_val, y_val)
    print(f"{rgb_accuracy:.3f}")

    # Build model_lab using pipeline with FunctionTransformer
    model_lab = Pipeline([
        ('rgb_to_lab', FunctionTransformer(rgb_to_lab_transform)),
        ('classifier', GaussianNB())
    ])
    model_lab.fit(X_train, y_train)
    
    # Print model_lab's accuracy score
    lab_accuracy = model_lab.score(X_val, y_val)
    print(f"{lab_accuracy:.3f}")

    # Visualize predictions and save plots
    plot_predictions(model_rgb)
    plt.savefig('predictions_rgb.png')
    
    plot_predictions(model_lab)
    plt.savefig('predictions_lab.png')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python colour_bayes.py <colour-data.csv>")
        sys.exit(1)
    main(sys.argv[1])
