import re
import pyodbc
import requests
from bs4 import BeautifulSoup

# The URL of the website you want to scrape
# url = 'https://time.ir'

# Replace with your SQL Server details
server = '192.168.110.200'
database = 'IPA_DW'
username = 'DWUser1'
password = 'xxx'
driver= '{ODBC Driver 18 for SQL Server}'

conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes;')
cursor = conn.cursor()
for year in range(1402, 1404):
    for month in range(1, 13):
        for day in range(1, 32):
            # https://www.time.ir/fa/event/list/0/1403/01/13
            URL = f'https://www.time.ir/fa/event/list/0/{year}/{month:2}/{day:2}'.replace(' ', '0')
            PersianDate = year * 10000 + month * 100  + day
            if PersianDate<14021211:
                print(f'{PersianDate} has been proccesed before')
            if month>6 and day>30:
                print(f'Invalid Date {PersianDate}')
                break
            html_content = requests.get(URL)
            soup = BeautifulSoup(html_content.text, 'html.parser')
            res = soup.find_all('li', class_='eventHoliday')

            print('+'*42, PersianDate)

            for s in res:
                x = re.findall(r'\n(.*)', s.text)
                print(f'{PersianDate} Extracted From {x[1].strip()}')
                #query = f'INSERT INTO [basic].[DimDateOccasion] (PersianDateKey, Title, isHoliday) VALUES ({PersianDate}, ''{x[1].strip()}'')'
                #print(query)
                query = '''If Exists(Select 1 From basic.dimDate Where PersianDateKey=?)
                    INSERT INTO [basic].[DimDateOccasion] (PersianDateKey, Title, isHoliday) VALUES (?, ?, ?)'''
                # Execute the query
                cursor.execute(query, PersianDate, PersianDate, x[1].strip(), 1)
                conn.commit()
                
conn.close()

# print(res)
# print('-'*42)
# x = re.findall(r'\n(.*)', res[0].text)

# print(x[1])





# Send a GET request to the website
#response = requests.get(url)
#print(response.text)

# # Check if the request was successful
# if response.status_code == 200:
#     # Parse the HTML content of the page with BeautifulSoup
#     soup = BeautifulSoup(response.text, 'html.parser')
    
#     # Now you can navigate and search the parse tree to extract data
#     # For example, to extract all text within <p> tags:
#     paragraphs = soup.find_all('p')
#     for paragraph in paragraphs:
#         print(paragraph.text)
# else:
#     print(f'Failed to retrieve the webpage. Status code: {response.status_code}')