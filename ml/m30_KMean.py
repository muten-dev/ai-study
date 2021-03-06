from sklearn.datasets import load_iris
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd

datasets = load_iris()

irisDF = pd.DataFrame(data=datasets.data, columns=datasets.feature_names)
print(irisDF)

kmean = KMeans(n_clusters=3, max_iter=300, random_state=66) 
# n_clusters: 3개의 라벨을 뽑을 것 (라벨 종류의 수)
# max_iter: 최대 반복 횟수
kmean.fit(irisDF)

results = kmean.labels_ # y value
print(results)
print(datasets.target)  # original y value

irisDF['cluster'] = kmean.labels_   # 클러스터링해서 생성한 y값
irisDF['target'] = datasets.target  # 원래의 y값

print(datasets.feature_names)
# ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)']
iris_results = irisDF.groupby(['target', 'cluster'])['sepal length (cm)'].count()
print(iris_results)