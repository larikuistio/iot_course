import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal, chi2
from scipy.spatial import distance
import pandas as pd
import scipy as sp

plt.rcParams["figure.figsize"] = (12, 8)

date = []
electricity = []
with open('electricity.txt', newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in csvreader:
        date.append(row[0])
        electricity.append(float(row[1]))

temperature = []
with open('temperatures.txt', newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in csvreader:
        temperature.append(float(row[1]))

# https://www.machinelearningplus.com/statistics/mahalanobis-distance/
data = np.array([electricity, temperature])
df = pd.DataFrame(data={'date': date, 'electricity': electricity, 'temperature': temperature})
df_x = df[['electricity', 'temperature']]

df2 = df_x - np.mean(df_x)
cov_mat = np.cov(df_x.values.T)
inv_mat = sp.linalg.inv(cov_mat)
left_term = np.dot(df2, inv_mat)
mahal = np.dot(left_term, df2.T)
df["mahalanobis"] = mahal.diagonal()

df['p_value'] = 1 - chi2.cdf(df['mahalanobis'], 2)
df = df[df.p_value >= 0.01]

df.plot(y='electricity', x='temperature', kind='scatter')
plt.show()

with open("data_no_outliers.txt", "w") as file:
    for data in df.values:
        file.write(data[0] + ", " + str(data[1]) + ", " + str(data[2]) + ", " + "\n")
