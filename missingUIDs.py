import csv
def collect():
    data = None
    data1 = None
    with open('eventdata.csv') as csvdata:
        d = csv.reader(csvdata)
        data = list(d)   
    with open('StudentDirectoryIDs.csv') as csvdata:
        d1 = csv.reader(csvdata)
        data1 = list(d1)
    foundemails = [i[0] for i in data1]
    allemails = [i[6] for i in data]
    count = 0 
    emails = set()
    for email in allemails:
        if email not in foundemails and email not in emails:
            print(email)
            emails.add(email)
            count+=1
    print(count)
collect() 