import csv
import urllib.request
import re

def collect():
    data = None
    with open('eventdata.csv') as csvdata:
        d = csv.reader(csvdata)
        data = list(d)
    with open('new_data.csv', 'w') as newdata:
        writer = csv.writer(newdata, delimiter=',')
        writer.writerow(["Email", "UID"])
        for row in data[1:]:
            email = row[6]
            if email.split('@')[1] == "berkeley.edu":
                try:
                    uid = get_uid(email.split('@')[0])
                except:
                    print("Connection error:", count)
                    print(row[4] + " " + row[5], email)
                if uid:
                    writer.writerow([email, uid])

def get_uid(email):
    url = "https://calnet-p2.calnet.berkeley.edu/directory/search.pl?search-type=email&search-base=student&search-term=" + email + "%40berkeley.edu&search=Search"
    res = urllib.request.urlopen(url).read().decode("utf8")
    m = re.findall(r'uid=([0-9]+)', res)
    return m[0] if m and len(m) == 1 else 0

collect()
