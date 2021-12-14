import csv
import os
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
import numpy as np

input = []

with open('events.csv', newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    next(csvreader)
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
if day:
        avg_consump = 0
        sum = 0
        for value in day:
            sum += float(value[1])
        avg_consump = sum / len(day)
        results.insert(len(results), [day[0][0], avg_consump])
        day = []


cities = [
    "Helsinki",
    "Tornio",
    "Lappeenranta",
    "Oulu",
    "Espoo",
    "Porvoo",
    "Jämsä",
    "Kouvola",
    "Rauma",
    "Vantaa",
    "Kokkola",
    "Tampere",
    "Imatra",
    "Joensuu",
    "Turku",
    "Kemi",
    "Jyväskylä",
    "Kotka",
    "Äänekoski",
    "Raahe",
    "Kuopio",
    "Lohja",
    "Lahti",
    "Pori",
]

weights = [1.75, 1.75, 1.75, 1.75, 1.75, 1.75, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.25, 1.25, 1.25, 1.25, 1.25, 1.25, 1, 1, 1, 1, 1, 1]


for city in cities:
    os.system("wget 'https://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=GetFeature&storedquery_id=fmi::observations::weather::daily::simple&place=" + city + "&starttime=" + results[0][0] + "&endtime=" + results[-1][0] + "' -O input/pred" + city + ".xml")


content = []
files = [None] * 24
for i, city in enumerate(cities):
    tmp = []
    tmp.append("input/pred" + city + ".xml")
    files[i] = tmp


dicts = []

for city in files:
    d = {}
    for filename in city:
        # Read the XML file
        with open(filename, "r") as file:
            # Read each line in the file, readlines() returns a list of lines
            content = file.readlines()
            # Combine the lines in the list into a string
            content = "".join(content)
            bs_content = bs(content, "lxml")

            result = bs_content.find_all("BsWfs:BsWfsElement".lower())

            for element in result:
                # Get tag with temperature data
                if element["gml:id"].endswith(".2"):
                    if "00:00:00" in list(element.children)[3].text.split("T")[1]:
                        # Parse date
                        # Parse average temperature
                        d[list(element.children)[3].text.split("T")[0]] = list(element.children)[7].text

    dicts.append(d)


days = dicts[0].keys()
avg_temps = []
for day in days:
    sum_temp = 0
    num = 0
    for i, d in enumerate(dicts):
        temp = d.get(day)
        if temp is not None:
            if temp != "NaN":
                sum_temp = sum_temp + float(temp) * weights[i]
                num = num + weights[i]
    avg_temps.append(sum_temp / num)

coeffs = [-171.76159, 1.91867, 10227.69325]

def fit_func(x, a, b, c):
	return a * x + b * x**2 + c

csv = []
dates = []
elec = []
pred = []

for i, data in enumerate(results):
    csv.append([data[0], data[1], avg_temps[i], fit_func(avg_temps[i], coeffs[0], coeffs[1], coeffs[2])])
    dates.append(data[0])
    elec.append(data[1])
    pred.append(fit_func(avg_temps[i], coeffs[0], coeffs[1], coeffs[2]))



plt.plot(dates, elec, label = "real electricity consumption")
plt.plot(dates, pred, label = "predicted electricity consumption")
plt.legend()
plt.show()
