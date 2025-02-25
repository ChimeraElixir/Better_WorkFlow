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
length = []
lengthHour = []
lengthMinute = []


html_text = requests.get("https://codeforces.com/contests")
soup = BeautifulSoup(html_text.text, "lxml")
print(soup.prettify())