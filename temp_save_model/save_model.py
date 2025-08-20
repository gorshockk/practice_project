import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Примерные данные
X = pd.read_csv(r"C:\practice\temp_save_model\X_train.csv")
y = pd.read_csv(r"C:\practice\temp_save_model\y_train.csv")

best_params={'max_depth': 9, 'min_samples_split': 5, 'n_estimators': 160}
model = RandomForestClassifier(max_depth=best_params['max_depth'],
    min_samples_split=best_params['min_samples_split'],
    n_estimators=best_params['n_estimators'],
    random_state=42)
model.fit(X, y)

# Сохраняем модель
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)
