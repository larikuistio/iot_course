from bs4 import BeautifulSoup as bs
import os

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
    os.system("wget 'https://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=GetFeature&storedquery_id=fmi::observations::weather::daily::simple&place=" + city + "&starttime=2014-11-30&endtime=2015-11-29' -O input/temp" + city + "0.xml")
    os.system("wget 'https://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=GetFeature&storedquery_id=fmi::observations::weather::daily::simple&place=" + city + "&starttime=2015-11-30&endtime=2016-11-29' -O input/temp" + city + "1.xml")
    os.system("wget 'https://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=GetFeature&storedquery_id=fmi::observations::weather::daily::simple&place=" + city + "&starttime=2016-11-30&endtime=2017-11-29' -O input/temp" + city + "2.xml")
    os.system("wget 'https://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=GetFeature&storedquery_id=fmi::observations::weather::daily::simple&place=" + city + "&starttime=2017-11-30&endtime=2018-11-29' -O input/temp" + city + "3.xml")
    os.system("wget 'https://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=GetFeature&storedquery_id=fmi::observations::weather::daily::simple&place=" + city + "&starttime=2018-11-30&endtime=2019-11-29' -O input/temp" + city + "4.xml")


content = []
files = [None] * 24
for i, city in enumerate(cities):
    tmp = []
    for j in range(5):
        tmp.append("input/temp" + city + str(j) + ".xml")
    files[i] = tmp


dates = []
temps = []
k = 0
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

            dates2 = []
            temps2 = []

            for element in result:
                # Get tag with temperature data
                if element["gml:id"].endswith(".2"):
                    if "00:00:00" in list(element.children)[3].text.split("T")[1]:
                        # Parse date
                        dates2.append(list(element.children)[3].text.split("T")[0])
                        # Parse average temperature
                        temps2.append(list(element.children)[7].text)
                        d[list(element.children)[3].text.split("T")[0]] = list(element.children)[7].text

            if k < 5:
                dates.extend(dates2)
            temps.append(temps2)
        k += 1
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


with open("temperatures.txt", "w") as file:
    for date, temp in zip(days, avg_temps):
        file.write(date + ", " + str(temp) + "\n")
