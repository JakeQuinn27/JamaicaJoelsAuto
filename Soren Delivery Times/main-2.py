from __future__ import print_function

import gspread
import os.path
import requests
import google
import csv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


JAMAICA_JOELS_ADDRESS = "37 w 13th ave, eugene, or 97401"
API_KEY = "AIzaSyAPnpMyoPF9J_of5txQlGGOF4Mq-k2hF4g"
API_SERVICE_NAME = 'sheets'
API_VERSION = 'v4'

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1vGm_PuCrGQwDTERnKf14xI4pnzZt_VfgsI5LTHg5RXI'
RANGE_NAME = 'July 27 - Oct 11!A1:A704'

CLIENT_SECRET_FILE: 'credentials.json'


def get_distance(origin, dest):
    dest = dest + ", Eugene, OR"
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins={}&destinations={}&units=imperial&key={}".format(origin, dest, API_KEY)

    return requests.request("GET", url)


def calculate_times():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

        times = []
        for row in values:
            distance = get_distance(JAMAICA_JOELS_ADDRESS, row[0]) 
            
            if distance.json()['rows'][0]['elements'][0]['duration']['text'] is IndexError:
                pass

            else:
                time = distance.json()['rows'][0]['elements'][0]['duration']['text']
                print(time)
                times.append([time])

        # Update the sheet
        range_ = 'July 27 - Oct 11!D1:D' + str(len(times))
        body = {
            'values': times
        }
        result = sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=range_,
            valueInputOption='RAW',
            body=body
        ).execute()

    except HttpError as err:
        print(err)


if __name__ == '__main__':
    addresses = calculate_times()
