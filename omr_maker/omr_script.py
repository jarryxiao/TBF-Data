import csv
file = open('omr_data.csv')
reader = csv.reader(file)
data = list(reader)
col_headers = data[0]