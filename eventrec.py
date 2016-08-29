import csv
import numpy as np
from queue import PriorityQueue as pq

""" State of events. """
event_to_index = {}
index_to_event = {}
event_index = 0

""" State of individuals. """
email_to_index = {}
index_to_email = {}
emails_to_events = {}
email_index = 0

""" State of the matrix array. """
zero_list = []
matrix_array = []
attendance = []

""" Opens eventdata.csv and populates event_to_index and index_to_event. """
with open('eventdata.csv') as csvfile:
    sheet = csv.reader(csvfile, delimiter= ',', quotechar='|')
    next(sheet)
    for row in sheet:

        status = row[18]
        if status == "Attending":
            status = 0.5
        else:
            status = 1

        event = str(row[0])
        email = str(row[6]).lower()
        if event not in event_to_index.keys():
            event_to_index[event] = event_index
            index_to_event[event_index] = event
            event_index += 1

        current_event = (event_to_index[event], status)
        if email not in email_to_index.keys():
            email_to_index[email] = email_index
            index_to_email[email_index] = email
            emails_to_events[email] = []
            email_index += 1
        try:
            emails_to_events[email].append(current_event)
        except:
            print(email)
    """ Creates an array of zeros the size of the number of events. """

    """ Creates an array of arrays of zeros the size of the number of email * the number of events. """
    j = 0
    matrix_array = []
    while j < email_index:
        matrix_array.append([0 for i in range(event_index)])
        j += 1
    """ Fills in .5 for an email that signed up for a ticket and 1 for an email that checked in. """
    for email in emails_to_events.keys():
        row = email_to_index[email]
        for col, val in emails_to_events[email]:
            matrix_array[row][col] = val

""" Creates a matrix where each row is an implicit user and each column is an implicit event. """
user_matrix = np.array(matrix_array)
g = "smccall@berkeley.edu"
print(user_matrix[email_to_index[g]])

def S(i, j):
    return np.linalg.norm(user_matrix[i] - user_matrix[j])

def kNN(k, email):
    guestindex = email_to_index[email]
    neighbors = pq(maxsize=k)
    for i in range(len(user_matrix)):
        if i != guestindex:
            simularity = -S(guestindex, i)
            if neighbors.full():
                neighbors.get()
            neighbors.put((simularity, index_to_email[i]))

    nearestneighbors = []
    while not neighbors.empty():
        i = neighbors.get()[1]
        nearestneighbors.append(i)

    return nearestneighbors

print(kNN(10, g))









