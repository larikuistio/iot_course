from bs4 import BeautifulSoup
import urllib.request
import re

url = 'https://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=GetFeature&storedquery_id=fmi::observations::weather::daily::simple&place=Oulu&starttime=2020-11-29&endtime=2021-11-29'
response = urllib.request.urlopen(url)
data = response.read()      # a `bytes` object
text = data.decode('utf-8') # a `str`;
soup = BeautifulSoup(text,'xml')
name = soup.find_all(attrs={"gml:id" : "BsWfsElement.1.2.2"})

p = re.compile("<BsWfs:ParameterValue>((|\-)[0-9]{1,2}\.[0-9])<\/BsWfs:ParameterValue>")
print(str(name))
m = p.match(str(name))
print(m.group())
