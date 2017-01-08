import csv
file = open('omr_data.csv')
reader = csv.reader(file)
data = list(reader)
col_headers = data[0]

class Person(object):
	def __init__(self, data_row):
		self.last_name = data_row[0]
		self.first_name = data_row[1]
		self.email = data_row[2]
		self.cell_phone = data_row[3]
		self.status = data_row[4]
		self.comm = data_row[5]
		self.div = data_row[6]
		self.proj = data_row[7]
		self.pos = data_row[8]
		self.join_date = data_row[9]
		self.major = data_row[10]
		self.bday = data_row[11]
		self.shirt_size = data_row[12]

	
