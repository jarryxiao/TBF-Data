from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from eventbrite import Eventbrite
import requests
import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def pull_from_sheet(row_id):
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1ABe3MOtf_YTuctgpc9FIT56F6pfi2o47Mj-0drxPB68'
    rangeName = 'Events In Progress!C' + str(row_id) + ':N' + str(row_id)
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])
    return values[0]

def format_date(date_str, time_str):
    print(date_str, time_str)
    date_lst = date_str.split("/")
    time_lst = time_str.split(":")
    d = datetime.datetime(int(date_lst[2]), int(date_lst[0]), int(date_lst[1]), hour=int(time_lst[0]) + 12, minute=int(time_lst[1][:2]))
    d = d + datetime.timedelta(hours=7)
    start = d.isoformat() + "Z"
    d = d + datetime.timedelta(hours=1, minutes=30)
    end = d.isoformat() + "Z"
    return start, end

def create_event(event_id):
    details = pull_from_sheet(event_id)
    title = details[2] + " " + details[0] + " at the Berkeley Forum"
    start_time, end_time = format_date(details[3], details[4])
    print(start_time, end_time)
    response = requests.post(
        "https://www.eventbriteapi.com/v3/events/",
        headers = {
            "Authorization": "Bearer QXBUB7AGT6TGOYTSXLT4",
        },
        data = {
            "event.name.html": "(TEST) " + title,
            "event.start.utc": start_time,
            "event.start.timezone": "America/Los_Angeles",
            "event.end.utc": end_time,
            "event.end.timezone": "America/Los_Angeles",
            "event.currency": "USD"
        },
        verify = True,  # Verify SSL certificate
    )
    print(response)




if __name__ == '__main__':
    #print(format_date("4/7/2016", "6:00 PM"))
    #pull_from_sheet(13)
    create_event(12)
