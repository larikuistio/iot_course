import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal, chi2
from scipy.spatial import distance
from scipy.optimize import curve_fit
import pandas as pd
import scipy as sp
import matplotlib

# https://machinelearningmastery.com/curve-fitting-with-python/
# Define data fitting function
def fit_func(x, a, b, c):
	return a * x + b * x**2 + c

df = pd.read_csv("data_no_outliers.txt", header=None)
coeffs, _ = curve_fit(fit_func, df[2], df[1])

print('y = %.5f * x + %.5f * x^2 + %.5f' % (coeffs[0], coeffs[1], coeffs[2]))
print(fit_func(-5, coeffs[0], coeffs[1], coeffs[2]))

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 18}

matplotlib.rc('font', **font)

plt.figure(figsize=(16, 10), dpi=80)
plt.scatter(df[2], df[1])
# define a sequence of inputs between the smallest and largest known inputs
x_line = np.arange(min(df[2]), max(df[2]), 1)
# calculate the output for the range
y_line = fit_func(x_line, coeffs[0], coeffs[1], coeffs[2])
# create a line plot for the mapping function

axes = plt.gca()
axes.xaxis.label.set_size(28)
axes.yaxis.label.set_size(28)
plt.xlabel("Temperature (°C)")
plt.ylabel("Power (MW)")
plt.plot(x_line, y_line, '--', color='red')
plt.show()

