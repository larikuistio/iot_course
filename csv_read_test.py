import csv
import matplotlib.pyplot as plt
from scipy import stats

input = []

with open('electricity_hourly.csv', newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in csvreader:
        input.insert(len(input), [ ((row[2]).split(' '))[0].strip('"'), row[4].strip('"') ])


i = 0
day = []
results = []
day.insert(len(day), input[0])
for item in input[1:len(input)]:
    if item[0] != day[0][0]:
        avg_consump = 0
        sum = 0
        for value in day:
            sum += float(value[1])
        avg_consump = sum / len(day)
        results.insert(len(results), [day[0][0], avg_consump])
        day = []
    day.insert(len(day), item)


with open("electricity.txt", "w") as file:
    for data in results:
        file.write(data[0] + ", " + str(data[1]) + "\n")

temps = []
with open('temperatures.txt', newline='') as csvfile:
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
