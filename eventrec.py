import csv
import numpy as np
from queue import PriorityQueue as pq


with open('eventdata.csv') as csvfile:
    rdr = csv.reader(csvfile)
    data = next(r)
    emails = {}
    nametoemails = {}
    emailtonames = {}
    for row in rdr:
        name = row[4] + " " + row[5]
        name = name.lower()
        email = row[6].lower()
        tix = int(row[7])

        if name not in attendees and email not in emails:
            emails[email] = tix
            attendees[name] = tix
            nametoemails[name] = [email]
            emailtonames[email] = [name]
        elif name not in attendees:
            emailtonames[email] += [name]
            attendees[emailtonames[email][0]] += tix
            emails[email] += tix
        elif email not in emails:
            nametoemails[name] += [email]
            attendees[name] += tix
            emails[nametoemails[name][0]] += tix
        else:
            attendees[name] += tix
            emails[email] += tix
        total += tix
        

def S(i, j):
    return np.linalg.norm(UM[i] - UM[j])

def kNN(k, guest):
    guestindex = guesttoindex[guest]
    neighbors  = pq(maxsize=k)
    for i in range(len(UM)):
        if i != guestindex:
            simularity = -S(guestindex, i)
            if !neighbors.full():
                neighbors.get()
            neighbors.put((simularity, indextoguest[i]))

    nearestneighbors = []
    while not neighbors.empty():
        i = neighbors.get()[1]
        name = indextoguest[i]
        nearestneighbors.append(name)

    return nearestneighbors










