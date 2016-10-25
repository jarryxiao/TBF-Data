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

def get_description(descpt):
    """Event Details:

    [WRITE NAME OF EVENT IN ALL CAPS]

    [Copy/paste Event Description from GIR or Facebook event page]

    Date: [put in date]
    Time: [put in time] (see below for more details about admission)
    Location: [put in location hall/building]

    Admission

    This event is open to the public. Entry to the event will be open to ticketholders and, space-permitting, a limited number of walk-ins. Ticketholders are encouraged to arrive early to maximize their chances of getting in. Having a ticket does not guarantee access to the event but does give the ticketholder priority over walk-ins until [TIME] p.m., at which point walk-ins and ticketholders will have equal access to remaining seats. Our standard event policies apply. What follows is an overview of the admissions timeline. It may be subject to revisions as the event approaches. Seating in the venue is first-come, first served.

    [TIME – 1 hour before event start time] p.m.  Event Admission Opens for Ticket Holders

    [TIME – 10 min before event start time] p.m.  Event Admission No Longer Guaranteed for Ticket Holders

    [TIME – 10 min before event start time]  p.m.  Admission Opens for Walk-Ins (Limited Seating)

    [TIME – 5 min before event start time]  p.m.  Admission Closed (No Late Seating)

    [TIME]  p.m.  Event Begins

    More details will be shared very soon here and on our Facebook page. We encourage that you “Like” our Facebook page, The Berkeley Forum, to keep up to date on Forum events.

    Note on Tickets

    Tickets are non-transferable. While you may purchase a ticket on someone's behalf, their name must be listed on the ticket. All attendees will be asked to present a Valid ID at the venue that matches the name on the ticket.

    All tickets sales are final. Tickets are non-transferable and non-refundable.

    To secure a seat for more than one person, simply fill out the form once again for each subsequent person with his or her information.

    Please visit our website for a complete list of event policies.
    """

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


def extract_event_id(event):
    url = event.url
    url = url.split('=')
    return url[1]


def update_ticket_types(event, ticketclass):
    response = requests.post(
        "https://www.eventbriteapi.com/v3/events/" + extract_event_id(event) + "/ticket_classes/" + ticketclass,
        headers = {
            "Authorization": "Bearer QXBUB7AGT6TGOYTSXLT4",
        },
        data = {
            "event.name.html": "(TEST) " + title,
            "event.start.utc": "2018-01-31T13:00:00Z",
            "event.start.timezone": "America/Los_Angeles",
            "event.organizer_id": "The Berkeley Forum"
            "event.end.utc": "2018-05-31T13:00:00Z",
            "event.end.timezone": "America/Los_Angeles",
            "event.currency": "USD"
        },
        verify = True,  # Verify SSL certificate
    )


if __name__ == '__main__':
<<<<<<< HEAD
    create_event(16)
    create_event(17)
=======
    #print(format_date("4/7/2016", "6:00 PM"))
    #pull_from_sheet(13)
    create_event(12)
>>>>>>> 73d54c04594edeadf805f47f921ce600051522ba
