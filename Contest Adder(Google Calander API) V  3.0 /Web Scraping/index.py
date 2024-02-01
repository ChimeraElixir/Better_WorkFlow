from bs4 import BeautifulSoup
import pandas as pd
import requests
from datetime import datetime, timedelta

import sys

# # For getting input from input.txt file
# sys.stdin = open("input.txt", "r")

# Printing the Output to output.txt file
sys.stdout = open("output.html", "w")

contestNames = []
contestStart = []
timeHour = []
timeMinute = []


html_text = requests.get("https://codeforces.com/contests")
soup = BeautifulSoup(html_text.text, "lxml")
table = soup.find("table").find_all("td")

for i in range(0, len(table), 6):
    contestNames.append(table[i].text.strip())

for i in contestNames:
    print(i)

for i in range(2, len(table), 6):
    contestStart.append(table[i].text.strip())

for i in contestStart:
    print(i)

for i in range(3, len(table), 6):
    hour, minute = table[i].text.strip().split(":")
    timeHour.append(hour)
    timeMinute.append(minute)


for i, j in timeHour, timeMinute:
    print(i)
    print(j)


df = pd.DataFrame({"Name": contestNames,"Start": contestStart,"ContestHour": timeHour, "ContestMinutes": timeMinute,})

print(len(contestNames),len(contestStart),len(timeHour),len(timeMinute))
print(df)
df.to_csv("CodeforceCalander.csv")
