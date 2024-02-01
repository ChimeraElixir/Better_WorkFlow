import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from httplib2 import Http
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


SCOPES = ["https://www.googleapis.com/auth/calendar"]

API_KEY = "AIzaSyBbzLoF1y_ktgaosxqQyChJyACBoUOeOVo"


def main():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        # service = build('calendar', 'v3', credentials=creds)
        service = build("calendar", "v3", credentials=creds)

        df = pd.read_csv(
            "/Web Scraping/CodeforceCalander.csv"
        )
        # print(df)
        Summary = df["Name"]
        DateTime = df["Start"]
        hour = df["ContestHour"]
        minute = df["ContestMinutes"]

        for i in range(df.shape[0]):
            start_time = datetime.strptime(DateTime[i], "%b/%d/%Y %H:%M")
            end_time = start_time + timedelta(
                hours=int(hour[i]), minutes=int(minute[i])
            )
            TimeZone = "Asia/Kolkata"

            events_result = (
                service.events()
                .list(
                    calendarId="primary",
                    timeMin=str(start_time.strftime("%Y-%m-%dT%H:%M:%S" + "+05:30")),
                    timeMax=str(end_time.strftime("%Y-%m-%dT%H:%M:%S" + "+05:30")),
                    maxResults=1,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )

            event = events_result["items"]

            # events = events_result.get("items", [])

            ##### events is a dict with elements #####

            # {
            #     "kind": "calendar#events",
            #     "etag": '"p32sf9il0la4o80o"',
            #     "summary": "gaurav94266@gmail.com",
            #     "description": "",
            #     "updated": "2024-02-01T04:43:46.579Z",
            #     "timeZone": "Asia/Kolkata",
            #     "accessRole": "owner",
            #     "defaultReminders": [{"method": "popup", "minutes": 30}],
            #     "items": [
            #         {
            #             "kind": "calendar#event",
            #             "etag": '"3413525248052000"',
            #             "id": "0tsmvvsdgrb94l0jaojdc17au8",
            #             "status": "confirmed",
            #             "htmlLink": "https://www.google.com/calendar/event?eid=MHRzbXZ2c2RncmI5NGwwamFvamRjMTdhdTggZ2F1cmF2OTQyNjZAbQ",
            #             "created": "2024-02-01T04:43:44.000Z",
            #             "updated": "2024-02-01T04:43:44.026Z",
            #             "summary": "Codeforces Round (Div. 3)",
            #             "description": "Codeforces Round (Div. 3)",
            #             "location": "Delhi",
            #             "creator": {"email": "gaurav94266@gmail.com", "self": True},
            #             "organizer": {"email": "gaurav94266@gmail.com", "self": True},
            #             "start": {
            #                 "dateTime": "2024-02-06T17:35:00+05:30",
            #                 "timeZone": "Asia/Kolkata",
            #             },
            #             "end": {
            #                 "dateTime": "2024-02-06T19:50:00+05:30",
            #                 "timeZone": "Asia/Kolkata",
            #             },
            #             "iCalUID": "0tsmvvsdgrb94l0jaojdc17au8@google.com",
            #             "sequence": 0,
            #             "attendees": [
            #                 {
            #                     "email": "gaurav94266@gmail.com",
            #                     "organizer": True,
            #                     "self": True,
            #                     "responseStatus": "needsAction",
            #                 }
            #             ],
            #             "reminders": {
            #                 "useDefault": False,
            #                 "overrides": [
            #                     {"method": "email", "minutes": 1440},
            #                     {"method": "popup", "minutes": 10},
            #                 ],
            #             },
            #             "eventType": "default",
            #         }
            #     ],
            # }

            if event[0]["summary"] != Summary[i]:
                event = {
                    "summary": str(Summary[i]),
                    "location": "Delhi",
                    "description": str(Summary[i]),
                    "start": {
                        "dateTime": str(
                            start_time.strftime("%Y-%m-%dT%H:%M:%S" + "+05:30")
                        ),
                        "timeZone": "Asia/Kolkata",  # Corrected timezone name
                    },
                    "end": {
                        "dateTime": str(
                            end_time.strftime("%Y-%m-%dT%H:%M:%S" + "+05:30")
                        ),  # Corrected time format
                        "timeZone": "Asia/Kolkata",
                    },
                    "attendees": [
                        {"email": "gaurav94266@gmail.com"},
                    ],
                    "reminders": {
                        "useDefault": False,
                        "overrides": [
                            {"method": "email", "minutes": 24 * 60},
                            {"method": "popup", "minutes": 10},
                        ],
                    },
                }

                event = (
                    service.events().insert(calendarId="primary", body=event).execute()
                )
                print(f"Event created: {event.get('htmlLink')}")


            else:
                print("Event already exist")

                

    except HttpError as error:
        print("An error occurred: %s" % error)


if __name__ == "__main__":
    main()
