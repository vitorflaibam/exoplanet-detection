import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def run():
    df = pd.read_csv("data/features.csv")
    X = df.drop(columns=['is_exoplanet', 'target_name']).values
    y = df['is_exoplanet'].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    clf = RandomForestClassifier()
    clf.fit(X_train, y_train)

    probas = clf.predict_proba(X_test)[:, 1]
    with open("models/probability_scores.txt", "w") as f:
        for p in probas:
            f.write(f"{p}\n")
    print("Probabilidade de ser exoplaneta salva em models/probability_scores.txt")

    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    with open("models/ml_results.txt", "w") as f:
        f.write(f"Acurácia do modelo: {acc}\n")
    print(f"Acurácia salva em models/ml_results.txt")
