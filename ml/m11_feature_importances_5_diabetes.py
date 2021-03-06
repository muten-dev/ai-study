from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.datasets import load_iris, load_breast_cancer, load_wine, load_boston, load_diabetes
from sklearn.model_selection import train_test_split

#1 Data
datasets = load_diabetes()
x_train, x_test, y_train, y_test = train_test_split(
    datasets.data, datasets.target, train_size=0.8, random_state=66
)

#2 Model
model = DecisionTreeRegressor(max_depth=5)
# model = RandomForestClassifier()

#3 Train
model.fit(x_train, y_train)

#4 Evaluate / Predict
acc = model.score(x_test, y_test)
print('acc: ', acc)

print(model.feature_importances_)

import matplotlib.pyplot as plt
import numpy as np

def plot_feature_importances_dataset(model):
    n_features = datasets.data.shape[1]
    plt.barh(np.arange(n_features), model.feature_importances_,
             align='center')
    plt.yticks(np.arange(n_features), datasets.feature_names)
    plt.xlabel("Feature Importances")
    plt.ylabel("Features")
    plt.ylim(-1, n_features)

plot_feature_importances_dataset(model)
plt.show()