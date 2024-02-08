from bs4 import BeautifulSoup
import pandas as pd
import requests
from datetime import datetime, timedelta

import sys

# # For getting input from input.txt file
# sys.stdin = open("input.txt", "r")

# Printing the Output to output.txt file
sys.stdout = open("output.txt", "w")

contestNames = []
contestStart = []
timeHour = []
timeMinute = []


html_text = requests.get("https://codeforces.com/contests")
soup = BeautifulSoup(html_text.text, "lxml")
table = soup.find("table").find_all("tr")[1:]

for row in table:
    columns = row.find_all("td")
    contestNames.append(columns[0].text.strip())
    start_time_str = columns[2].text.strip()
    contestStart.append(start_time_str)

    # Parsing start time to get hour and minute
    start_time = datetime.strptime(start_time_str, "%b/%d/%Y %H:%M")
    timeHour.append(start_time.strftime("%H"))
    timeMinute.append(start_time.strftime("%M"))


df = pd.DataFrame(
    {
        "Name": contestNames,
        "Start": contestStart,
        "ContestHour": timeHour,
        "ContestMinutes": timeMinute,
    }
)

# Save DataFrame to CSV
df.to_csv("CodeforcesContests.csv", index=False)


