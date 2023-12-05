from __future__ import print_function

import sys

import gspread
import os.path
import requests
import google
import csv
import ast

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

# The ID and range of the spreadsheet.
SPREADSHEET_ID = '1vGm_PuCrGQwDTERnKf14xI4pnzZt_VfgsI5LTHg5RXI'
DELIVERY_DATE_RANGE = input("Dates for Delivery Period: ")

CLIENT_SECRET_FILE = 'credentials.json'

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


    #try:
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    add_sheet(service)
    add_columns(service)
    add_data(service)


    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=f"{DELIVERY_DATE_RANGE}!B2:B").execute()
    values = result.get('values', [])



    if not values:
        print('No data found.')
        return

    try:

        count =  0
        for i in values:
            if '#' in str(i):
                values[count] = str(i).replace("#", '')
            count += 1

        times = []
        time2 = []
        for row in values:
            distance = get_distance(JAMAICA_JOELS_ADDRESS, row[0])
            time = distance.json()['rows'][0]['elements'][0]['duration']['text']
            duration = int(time[0:2]) * 2
            time2.append([duration])
            times.append([time])


            # Update the sheet
        range_ = f'{DELIVERY_DATE_RANGE}!D2:D'
        body = {
            'values': time2
        }

        result = sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=range_,
            valueInputOption='RAW',
            body=body
        ).execute()

        add_times(service)

    except HttpError as err:
        print(err)


def add_times(service):
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=f"{DELIVERY_DATE_RANGE}!C2:D").execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
        return

    try:
        total_mins = {}
        for i in values:

            if i[0] in total_mins.keys():
                total_mins[i[0]] = total_mins[i[0]] + int(i[1])
            else:
                total_mins[i[0]] = int(i[1])

        range_ = f'{DELIVERY_DATE_RANGE}!E2:G'
        values_to_write = []
        for i in total_mins:
            values_to_write.append([i, total_mins[i], round(float(total_mins[i])/60, 2)])

        body = {'values': values_to_write}
        result = sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=range_,
            valueInputOption='RAW',
            body=body
        ).execute()

    except HttpError as err:
        print(err)



def add_data(service):

    pathname = input("Paste direct pathname to greenbits download: ")
    test = []     
    with open(f'{pathname}', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            test.append([row[6], row[19], row[18]])

        resource = {
            "majorDimension": "ROWS",
            "values": test
        }
        response = service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            valueInputOption='USER_ENTERED',
            range=DELIVERY_DATE_RANGE,
            body=resource
        ).execute()

    

def add_sheet(service):

    spreadsheets = service.spreadsheets()

    body = {
        'requests': [{
            'addSheet': {
                'properties': {
                    'title': DELIVERY_DATE_RANGE
                }
            }
        }]
    }

    response = spreadsheets.batchUpdate(
        spreadsheetId='1vGm_PuCrGQwDTERnKf14xI4pnzZt_VfgsI5LTHg5RXI',
        body=body
    ).execute()
                     
    print("fuck my ass kenny g")
    return


def add_columns(service):
    start_column = 'A'
    end_column = 'G'

    column_names = [['Date', 'Address', 'Driver (individual) ',
                     'Minutes (individual)', 'Driver (Total)',
                     'Minutes (Total)', 'Hours (Minutes/60)']]

    range_ = f'{DELIVERY_DATE_RANGE}!{start_column}1:{end_column}1'
    body = {'values': column_names}

    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID, range=range_,
        valueInputOption='RAW', body=body
    ).execute()





calculate_times()
