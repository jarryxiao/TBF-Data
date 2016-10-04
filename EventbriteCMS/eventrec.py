"""
    Processing the Eventbrite file. Designed to pull all the files and generate a model for
    how event time and day, as well as venue, affects event attendance.
"""

EVENTS = {

        "Angus King": 24669690709,

        }

import requests

# Helper method to get the Eventbrite data (returns JSON). The extension parameter is used
# exclusively to determine whether or not to get the attendee data.
def eventbrite_request(event_name, event_id, extension=""):
    print("Downloading Eventbrite Data")

    details_url = "https://www.eventbriteapi.com/v3/events/{0}/".format(event_id) + extension
    details_request = requests.get(
        details_url,
        headers = {
            "Authorization": "Bearer QXBUB7AGT6TGOYTSXLT4",
        },
        verify = True,
    )

    if details_request:
        details = details_request.json()
    else:
        #Figure out some sort of graceful exit strategy
        error_string = "Request Failed! No event details available for " + event_name
        print(error_string)
        details = None

    print("Finished Retrieving Eventbrite Data")

    return details

def get_venue(id):
    details_url = "https://www.eventbriteapi.com/v3/venues/{0}/".format(id)
    details_request = requests.get(
        details_url,
        headers = {
            "Authorization": "Bearer QXBUB7AGT6TGOYTSXLT4",
        },
        verify = True,
    )

    if details_request:
        details = details_request.json()
    else:
        #Figure out some sort of graceful exit strategy
        error_string = "Request Failed! No venue details available!"
        print(error_string)
        details = None

    return details


def get_event_data(event_name, event_id):

    event_details = eventbrite_request(event_name, event_id) 
    attendee_details = eventbrite_request(event_name, event_id, extension="attendees/")

    return (event_details, attendee_details)

def get_all_events():
    
    all_events = []
    for event_name, event_id in EVENTS.items():
        details = get_event_data(event_name, event_id)
        all_events.append(details) 

    return the_events


def get_timebox():
    print("Not implemented yet")


# Convenience method to return a tuple with the salient attendance details
# required to normalize by date/time
def parse_details(details, attended, estimate):
    time = details["start"]["local"] 
    timebox = get_timebox(time)
    attendance = len(attended["attendees"])
    return (timebox, attendance, estimate)


def group_by_venue():
    all_events = get_all_events()
    # Estimated attendances for all the events.
    # This should be a dict, mapped event_name => attendance_estimate
    estimates = get_attendance_estimates()
    
    by_venue = {}
    for event in all_events:
        # TODO: Can you just make it: details, attended = event ?
        details, attended = event[0], event[1]
        venue_id = details["venue_id"]
        venue_name = get_venue(venue_id)["name"]
        details_tuple = parse_details(details, attended, estimates[venue_name]) 
        if by_venue[venue_name]:
            by_venue[venue_name].append(details_tuple)
        else:
            by_venue[venue_name] = [details_tuple]

    return by_venue


def get_deltas():
    by_venue = group_by_venue()
    # Dictionary of the adjustments 
    time_deltas = {}

    for venue, details in by_venue.items():
        timebox, attended, estimate = details
        # Mult by 1.0 for Python 2.7 compatibility
        delta = (estimate * 1.0) / attended  
        if time_deltas[timebox]:
            time_deltas[timebox].append(delta)
        else:
            time_deltas[timebox] = [delta]

    return time_deltas

def normalize_by_time():
    # TODO: Make this analysis more sophisticated (if possible)
    # Right now, it's just a simple averaging of all the deltas for a timebox

    time_deltas = get_deltas()
    time_delta_avg = {}
    for time, deltas in time_deltas.items():
        average = (sum(deltas) * 1.0) / len(deltas)
        time_delta_avg[time] = average

    return time_delta_avg
