import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestClassifier


def main():
    if len(sys.argv) != 4:
        print("Usage: python weather_city.py <labelled_csv> <unlabelled_csv> <output_csv>")
        sys.exit(1)
    labelled_file = sys.argv[1]
    unlabelled_file = sys.argv[2]
    output_file = sys.argv[3]

    # Load labelled data
    data = pd.read_csv(labelled_file)
    X = data.drop(columns=['city', 'year']).values
    y = data['city'].values

    # Split into training and validation sets
    X_train, X_valid, y_train, y_valid = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Build pipeline: scale features then classify
    pipeline = make_pipeline(
        MinMaxScaler(),
        RandomForestClassifier(n_estimators=100, random_state=42)
    )

    # Train and evaluate
    pipeline.fit(X_train, y_train)
    score = pipeline.score(X_valid, y_valid)
    print(f"{score:.3f}")

    # Analyze misclassifications (commented out for submission)
    # df = pd.DataFrame({'truth': y_valid, 'prediction': pipeline.predict(X_valid)})
    # print(df[df['truth'] != df['prediction']])

    # Load unlabelled data and predict cities
    unlab = pd.read_csv(unlabelled_file)
    X_unlab = unlab.drop(columns=['city', 'year']).values
    preds = pipeline.predict(X_unlab)

    # Save predictions to output file
    pd.Series(preds).to_csv(output_file, index=False, header=False)


if __name__ == '__main__':
    main()
