import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal, chi2, dweibull
from scipy.spatial import distance
import pandas as pd
import scipy as sp
import seaborn as sns
from fitter import Fitter, get_common_distributions, get_distributions
import matplotlib

plt.rcParams["figure.figsize"] = (16, 10)

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

"""
sns.set_style('white')
sns.set_context("paper", font_scale = 2)
sns.displot(data=df, x="electricity", kind="hist", bins = 100, aspect = 1.5)
elec = df["electricity"].values
f = Fitter(elec, distributions=['dweibull'])
f.fit()
print(f.summary())
print(f.get_best(method = 'sumsquare_error'))
print(max(df['mahalanobis']))
print(dweibull.ppf((1-0.05), 1.5625551023293938, loc=6.456753586877175, scale=8.143723948957824))
print(dweibull.ppf((1-0.05), 1.5374460061967312, loc=9487.661221445767, scale=1340.8965894936905))
df['p_value'] = 1 - dweibull.cdf(df['mahalanobis'], 1.5625551023293938, loc=6.456753586877175, scale=8.143723948957824)
"""

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 18}

matplotlib.rc('font', **font)

df['p_value'] = 1 - chi2.cdf(df['mahalanobis'], 2)
df = df[df.p_value >= 0.01]
print(len(df))
plot = df.plot(y='electricity', x='temperature', kind='scatter')
plot.set_xlabel("Temperature (°C)")
plot.set_ylabel("Power (MW)")
plot.set_xlim(-26,26)
plot.set_ylim(6000,14500)
axes = plt.gca()
axes.xaxis.label.set_size(28)
axes.yaxis.label.set_size(28)
plt.show()


with open("data_no_outliers.txt", "w") as file:
    for data in df.values:
        file.write(data[0] + ", " + str(data[1]) + ", " + str(data[2]) + ", " + "\n")
