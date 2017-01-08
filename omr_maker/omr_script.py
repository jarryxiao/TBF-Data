import csv
file = open('omr_data.csv')
reader = csv.reader(file)
data = list(reader)