import requests
import bs4
import urllib


def pring(x):
    for i in x:
        print(i)

def get_schedule_table(url):
   data_table = []
   response = urllib.request.urlopen(url)
   doc = bs4.BeautifulSoup(response)
   count = 0

   tables = doc.find_all('tr')
   for i in tables:
      i = i.find_all("td")
      i = [ele.text.strip() for ele in i]
      if 'no classes' in str(i).lower():
            if i not in data_table:
               data_table.append(i)
      
      
   return data_table

y = get_schedule_table('https://www.fit.edu/registrar/academic-calendar/fall-2022/')
