import csv
import matplotlib.pyplot as plt
from scipy import stats


def find_outliers(col):
    z = np.abs(stats.zscore(col))
    idx_outliers = np.where(z > 3, True, False)


input = []

with open('events.csv', newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in csvreader:
        input.insert(len(input), [ ((row[2]).split(' '))[0].strip('"'), row[4].strip('"') ])

i = 0
day = []
results = []
j = 0
for item in input[1:len(input)]:
    j = len(str(item).split(':00:00'))
    if j != 5:
        continue
    else:
        day.insert(len(day), item)
        i += 1
        if i == 24:
            avg_consump = 0
            sum = 0
            for value in day:
                sum += float(value[1])
            avg_consump = sum / 24
            results.insert(len(results), [day[0][0], avg_consump])
            i = 0
            day = []


temps = []
with open('temperature.txt', newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in csvreader:
        temps.insert(len(input), [ row[0], float(row[1].strip(' ')) ])


x = []
y = []


for temp, consump in zip(temps, results):
    x.insert(len(x), temp[1])
    y.insert(len(y), consump[1])

slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)

xx = x
yy = [i * slope + intercept for i in xx]

print(slope)
print(intercept)

plt.plot(x, y, 'o')
plt.plot(xx, yy)
plt.show()

print(results)