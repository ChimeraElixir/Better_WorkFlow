from bs4 import BeautifulSoup
import pandas as pd
import requests
from datetime import datetime, timedelta, timezone, tzinfo

import sys

# # For getting input from input.txt file
# sys.stdin = open("input.txt", "r")

# Printing the Output to output.txt file
sys.stdout = open("output.txt", "w")

contestNames = []
DateTime = []
length=[]
lengthHour = []
lengthMinute = []


html_text = requests.get("https://codeforces.com/contests")
soup = BeautifulSoup(html_text.text, "lxml")
table = soup.find("table").find_all("tr")[1:]

for row in table:
    columns = row.find_all("td")
    
    contestNames.append(columns[0].text.strip())
    

    start_time = columns[2].text.strip()
    
   
    start_time = datetime.strptime(start_time, "%b/%d/%Y %H:%M")
    start_time = start_time + timedelta(hours=2, minutes=30)

    DateTime.append(str(start_time))

    length.append(columns[3].text.strip())


# print(lengthHour)
# print(lengthMinute)


df = pd.DataFrame(
    {
        "Name": contestNames,
        "Start": DateTime,
        "Length":length
    }
)

# Save DataFrame to CSV
df.to_csv("CodeforcesContests.csv", index=False)
