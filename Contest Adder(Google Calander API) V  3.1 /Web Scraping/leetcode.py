from bs4 import BeautifulSoup
import pandas as pd
import requests
from datetime import datetime, timedelta

import sys

# # For getting input from input.txt file
# sys.stdin = open("input.txt", "r")

# Printing the Output to output.txt file
sys.stdout = open("./output.html", "w")

html_text = requests.get("https://leetcode.com/contest/")
soup = BeautifulSoup(html_text.text, "lxml")

print(soup.find("div", class_="swiper-wrapper"))
# print(soup)
