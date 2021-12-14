from bs4 import BeautifulSoup as bs
#import urllib.request as req
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

#for city in cities:
#    req.urlretrieve("https://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=GetFeature&storedquery_id=fmi::observations::weather::daily::simple&place=" + city + "&starttime=2016-11-29&endtime=2017-11-28", "input/temp" + city + "0.xml")
#    req.urlretrieve("https://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=GetFeature&storedquery_id=fmi::observations::weather::daily::simple&place=" + city + "&starttime=2017-11-29&endtime=2018-11-28", "input/temp" + city + "1.xml")
#    req.urlretrieve("https://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=GetFeature&storedquery_id=fmi::observations::weather::daily::simple&place=" + city + "&starttime=2018-11-29&endtime=2019-11-28", "input/temp" + city + "2.xml")
#    req.urlretrieve("https://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=GetFeature&storedquery_id=fmi::observations::weather::daily::simple&place=" + city + "&starttime=2019-11-29&endtime=2020-11-28", "input/temp" + city + "3.xml")
#    req.urlretrieve("https://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=GetFeature&storedquery_id=fmi::observations::weather::daily::simple&place=" + city + "&starttime=2020-11-29&endtime=2021-11-28", "input/temp" + city + "4.xml")

for city in cities:
    os.system("wget 'https://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=GetFeature&storedquery_id=fmi::observations::weather::daily::simple&place=" + city + "&starttime=2016-11-29&endtime=2017-11-28' -O input/temp" + city + "0.xml")
    os.system("wget 'https://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=GetFeature&storedquery_id=fmi::observations::weather::daily::simple&place=" + city + "&starttime=2017-11-29&endtime=2018-11-28' -O input/temp" + city + "1.xml")
    os.system("wget 'https://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=GetFeature&storedquery_id=fmi::observations::weather::daily::simple&place=" + city + "&starttime=2018-11-29&endtime=2019-11-28' -O input/temp" + city + "2.xml")
    os.system("wget 'https://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=GetFeature&storedquery_id=fmi::observations::weather::daily::simple&place=" + city + "&starttime=2019-11-29&endtime=2020-11-28' -O input/temp" + city + "3.xml")
    os.system("wget 'https://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=GetFeature&storedquery_id=fmi::observations::weather::daily::simple&place=" + city + "&starttime=2020-11-29&endtime=2021-11-28' -O input/temp" + city + "4.xml")


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

for city in files:
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

            #dates2.reverse()
            #temps2.reverse()
            if k < 5:
                dates.extend(dates2)
            temps.append(temps2)
        k += 1

#dates.reverse()
#temps.reverse()


temps2 = [[]] * 24
i = 0
j = 0
for temp in temps:
    if i == 0:
        temps2[j] = temp
        i += 1
    elif i == 4:
        temps2[j].extend(temp)
        i = 0
        j += 1
    else:
        temps2[j].extend(temp)
        i += 1
temps = temps2

for i, city in enumerate(temps):
    for j, value in enumerate(city):
        temps[i][j] = float(temps[i][j])

temps_avg = [0] * len(temps[0])
for i, city in enumerate(temps):
    for j, value in enumerate(city):
        temps_avg[j] = temps_avg[j] + value * weights[i]

for i in range(len(temps_avg)):
    temps_avg[i] = temps_avg[i] / 33

with open("temperatures.txt", "w") as file:
    for date, temp in zip(dates, temps_avg):
        file.write(date + ", " + str(temp) + "\n")
