import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from skimage.color import lab2rgb, rgb2lab, rgb2hsv
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
import sys


OUTPUT_TEMPLATE = (
    'Bayesian classifier:     {bayes_rgb:.3f}  {bayes_convert:.3f}\n'
    'kNN classifier:          {knn_rgb:.3f}  {knn_convert:.3f}\n'
    'Rand forest classifier:  {rf_rgb:.3f}  {rf_convert:.3f}\n'
)


# representative RGB colours for each label, for nice display
COLOUR_RGB = {
    'red': (255, 0, 0),
    'orange': (255, 112, 0),
    'yellow': (255, 255, 0),
    'green': (0, 231, 0),
    'blue': (0, 0, 255),
    'purple': (185, 0, 185),
    'brown': (117, 60, 0),
    'pink': (255, 184, 184),
    'black': (0, 0, 0),
    'grey': (150, 150, 150),
    'white': (255, 255, 255),
}
name_to_rgb = np.vectorize(COLOUR_RGB.get, otypes=[np.uint8, np.uint8, np.uint8])


def plot_predictions(model, lum=67, resolution=300, input_space='rgb'):
    """
    Create a slice of LAB colour space with given luminance; predict with the model; plot the results.
    """
    wid = resolution
    hei = resolution
    n_ticks = 5

    # create a hei*wid grid of LAB colour values, with L=lum
    ag = np.linspace(-100, 100, wid)
    bg = np.linspace(-100, 100, hei)
    aa, bb = np.meshgrid(ag, bg)
    ll = lum * np.ones((hei, wid))
    lab_grid = np.stack([ll, aa, bb], axis=2)

    # convert to RGB for display
    X_display = lab2rgb(lab_grid)
    
    # prepare input for model based on what it was trained on
    if input_space == 'lab':
        X_model = lab_grid.reshape((-1, 3))
    elif input_space == 'hsv':
        X_rgb = lab2rgb(lab_grid)
        X_model = rgb2hsv(X_rgb.reshape(-1, 1, 3)).reshape(-1, 3)
    else:  # rgb
        X_model = lab2rgb(lab_grid).reshape((-1, 3))

    # predict and convert predictions to colours so we can see what's happening
    y_grid = model.predict(X_model)
    pixels = np.stack(name_to_rgb(y_grid), axis=1) / 255
    pixels = pixels.reshape((hei, wid, 3))

    # plot input and predictions
    plt.figure(figsize=(10, 5))
    plt.suptitle('Predictions at L=%g' % (lum,))
    plt.subplot(1, 2, 1)
    plt.title('Inputs')
    plt.xticks(np.linspace(0, wid, n_ticks), np.linspace(-100, 100, n_ticks))
    plt.yticks(np.linspace(0, hei, n_ticks), np.linspace(-100, 100, n_ticks))
    plt.xlabel('A')
    plt.ylabel('B')
    plt.imshow(X_display.reshape((hei, wid, -1)))

    plt.subplot(1, 2, 2)
    plt.title('Predicted Labels')
    plt.xticks(np.linspace(0, wid, n_ticks), np.linspace(-100, 100, n_ticks))
    plt.yticks(np.linspace(0, hei, n_ticks), np.linspace(-100, 100, n_ticks))
    plt.xlabel('A')
    plt.imshow(pixels)


def main():
    if len(sys.argv) != 2:
        print("Usage: python colour_predict.py <csv_file>")
        print("Example: python colour_predict.py colour-data.csv")
        sys.exit(1)
    
    data = pd.read_csv(sys.argv[1])
    X = data[['R', 'G', 'B']].values / 255  # normalize RGB to [0,1]
    y = data['Label'].values

    # Split into training and validation sets
    X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.25, random_state=42)

    # Convert RGB to LAB and HSV color spaces
    X_train_lab = rgb2lab(X_train.reshape(-1, 1, 3)).reshape(-1, 3)
    X_valid_lab = rgb2lab(X_valid.reshape(-1, 1, 3)).reshape(-1, 3)
    
    X_train_hsv = rgb2hsv(X_train.reshape(-1, 1, 3)).reshape(-1, 3)
    X_valid_hsv = rgb2hsv(X_valid.reshape(-1, 1, 3)).reshape(-1, 3)

    # Create models
    # Bayesian classifiers (GaussianNB)
    bayes_rgb_model = GaussianNB()
    bayes_convert_model = GaussianNB()  # Using LAB color space
    
    # k-NN classifiers
    knn_rgb_model = KNeighborsClassifier(n_neighbors=15, weights='distance')
    knn_convert_model = KNeighborsClassifier(n_neighbors=11, weights='distance')  # Using HSV color space
    
    # Random Forest classifiers
    rf_rgb_model = RandomForestClassifier(n_estimators=100, max_depth=15, random_state=42)
    rf_convert_model = RandomForestClassifier(n_estimators=100, max_depth=15, random_state=42)  # Using LAB color space

    # Train models
    bayes_rgb_model.fit(X_train, y_train)
    bayes_convert_model.fit(X_train_lab, y_train)
    
    knn_rgb_model.fit(X_train, y_train)
    knn_convert_model.fit(X_train_hsv, y_train)
    
    rf_rgb_model.fit(X_train, y_train)
    rf_convert_model.fit(X_train_lab, y_train)

    # Generate prediction plots for each model
    models = [bayes_rgb_model, bayes_convert_model, knn_rgb_model, knn_convert_model, rf_rgb_model, rf_convert_model]
    input_spaces = ['rgb', 'lab', 'rgb', 'hsv', 'rgb', 'lab']
    
    for i, (m, space) in enumerate(zip(models, input_spaces)):
        plot_predictions(m, input_space=space)
        plt.savefig('predictions-%i.png' % (i,))
        plt.close()  # Close the figure to save memory

    # Calculate scores and print results
    print(OUTPUT_TEMPLATE.format(
        bayes_rgb=bayes_rgb_model.score(X_valid, y_valid),
        bayes_convert=bayes_convert_model.score(X_valid_lab, y_valid),
        knn_rgb=knn_rgb_model.score(X_valid, y_valid),
        knn_convert=knn_convert_model.score(X_valid_hsv, y_valid),
        rf_rgb=rf_rgb_model.score(X_valid, y_valid),
        rf_convert=rf_convert_model.score(X_valid_lab, y_valid),
    ))


if __name__ == '__main__':
    main()
