import csv
import numpy as np

""" State of events. """
event_to_index = {}
index_to_event = {}
event_index = 0

""" State of individuals. """
email_to_index = {}
index_to_email = {}
email_index = 0

""" State of the matrix array. """
zero_list = []
matrix_array = []
attendance = []

""" Opens eventdata.csv and populates event_to_index and index_to_event. """
with open('eventdata.csv') as csvfile:
	sheet = csv.reader(csvfile, delimiter= ',', quotechar='|')
	for row in sheet:
		attendance.append(str(row[18]))
		event = str(row[0])
		email = str(row[6]).lower()
		if event not in event_to_index.keys():
			event_to_index[event] = event_index
			index_to_event[event_index] = event
			event_index += 1
		if email not in email_to_index.keys() and '@' in email:
			email_to_index[email] = email_index
			index_to_email[email_index] = email
			email_index += 1
	""" Creates an array of zeros the size of the number of events. """
	i = 0
	zero_list = []
	while i < event_index + 1: # event_index + 1 == number of events
		zero_list.append(0)
		i += 1
	""" Creates an array of arrays of zeros the size of the number of email * the number of events. """
	j = 0
	matrix_array = []
	while j < email_index + 1:
		matrix_array.append(zero_list)
		j += 1
	""" Fills in .5 for an email that signed up for a ticket and 1 for an email that checked in. """
	sheet = csv.reader(csvfile, delimiter= ',', quotechar='|')
	for row in attendance:
		if str(row) == "Attending":
			print("a")
			# email_position = email_to_index[row[6]]
			# event_position = event_to_index[row[0]]
			# matrix_array[email_position][event_position] = .5
		if str(row) == "Checked In":
			print("b")
			# email_position = email_to_index[row[6]]
			# event_position = event_to_index[row[0]]
			# matrix_array[email_position][event_position] = 1

""" Creates a matrix where each row is an implicit user and each column is an implicit event. """
user_matrix = np.matrix(matrix_array)
print(user_matrix)