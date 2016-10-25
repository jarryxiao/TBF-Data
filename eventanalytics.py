import csv
import xlwt
from xlutils.copy import copy # http://pypi.python.org/pypi/xlutils
from xlrd import open_workbook # http://pypi.python.org/pypi/xlrd
from xlwt import easyxf # http://pypi.python.org/pypi/xlwt


total = 0
#total_spr_2016 = 0
attendees = {}
#attendees_2016 = {}
emails = {}
nametoemails = {}
emailtonames = {}
# emails_2016 = {}
# nametoemails2016 = {}
# emailtonames2016 = {}
events = {}
with open('eventdata3.csv') as csvfile:


    tickettypes = set()
    r = csv.reader(csvfile)
    data = next(r)

    for row in r:
        name = row[4] + " " + row[5]
        name = name.lower()

        email = row[6].lower()
        tix = int(row[7])
        event = row[0]
        checkedin = row[13]=="Checked In"

        # if event not in events:
        #     events[event] = {}
        #     events[event]["Total"] = [0,0]
        
        # TT = row[8]  

        # if TT not in events[event]:
        #     events[event][TT] = [0,0] 

        # if checkedin:
        #     events[event]["Total"][0] += tix 
        #     events[event][TT][0] += tix
        # else:
        #     events[event]["Total"][1] += tix
        #     events[event][TT][1] += tix
        if checkedin:
            if name == "hansmeet singh":
                print(name)
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


with open('walkin.csv') as csvfile:
    r1 = csv.reader(csvfile)
    for row in r1:
        name = row[1].lower()
        email = row[2].lower()
        if name == "hansmeet singh":
            print(name)

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

    freqs = [(a, attendees[a]) for a in attendees.keys() if attendees[a] > 3]
    freqs = sorted(freqs, key=lambda x: -x[1]) 
    freqs = [(f[0], nametoemails[f[0]], f[1]) for f in freqs] 

with open('freqguests.csv', 'w') as csvfile:
    w = csv.writer(csvfile, delimiter=',')
    for f in freqs:
        w.writerow([f[0],f[1],f[2]])
    print(len(freqs))
        # if int(row[3][:4]) == 2016:
        #     if name not in attendees_2016 and email not in emails_2016:
        #         attendees_2016[name] = tix
        #         emails_2016[email] = tix
        #         nametoemails2016[name] = [email]
        #         emailtonames2016[email] = [name]
        #     elif name not in attendees_2016:
        #         emailtonames2016[email] += [name]
        #         attendees_2016[emailtonames2016[email][0]] += tix
        #         emails_2016[email] += tix
        #     elif email not in emails_2016:
        #         nametoemails2016[name] += [email]
        #         attendees_2016[name] += tix
        #         emails_2016[nametoemails2016[name][0]] += tix
        #     else:
        #         attendees_2016[name] += tix
        #         emails_2016[email] += tix
        #     total_spr_2016 += tix

    # for event in events:
    #     print(event)
    #     for i in range(len(events[event])):
    #         if i == 0:
    #             ttype = "Event Total"
    #         elif i == 1:
    #             ttype = "Student"
    #         elif i == 2:
    #             ttype = "General Admission"
    #         else:
    #             ttype = "Other"
    #         print(ttype + " Checked In: " + str(events[event][i][0])) 
    #         print(ttype + " Attending: " + str(events[event][i][1]))
    #         if events[event][i][0]+events[event][i][1] > 0:
    #             print("Ratio: " + str(events[event][i][0]/(events[event][i][0]+events[event][i][1])))
    #         else:
    #             print("Ratio: " + "N/A")
    # print("Total attendance since 2014: " + str(total))
    # print("Total attendance last semester: " + str(total_spr_2016))
    # unique = len(attendees)
    # unique2016 = len(attendees_2016)
    # print("Unique attendees since 2014: " + str(unique))
    # print("Unique attendees last semester: " + str(unique2016))

    # repeat = sum(f[1] for f in freqs)
    # print(unique + repeat - len(freqs), total)
    # freqs2016 = [(a, attendees_2016[a]) for a in attendees_2016.keys() if attendees_2016[a] > 1]
    # freqs2016 = sorted(freqs2016, key=lambda x: -x[1])
    # repeat2016 = sum(f[1] for f in freqs2016)
    # print(unique2016 + repeat2016 - len(freqs2016), total_spr_2016)
    # events = [(n, events[n]) for n in events.keys()]
    # events = sorted(events, key=lambda x: -x[1][1]/x[1][0])
    # workbook = open_workbook("Venue.xlsx")
    # worksheet = workbook.sheet_by_name("Sheet1")
    # wb = copy(workbook) # a writable copy (I can't read values out of this, only write to it)
    # w_sheet = wb.get_sheet(0) # the sheet to write to within the writable copy
    # i = 1
    # for event in events:
    #     w_sheet.write(i, 0, event)
    #     w_sheet.write(i, 1, "Attending")
    #     w_sheet.write(i, 2, "Checked In")
    #     w_sheet.write(i, 3, "Grand Total")
    #     i += 1
    #     total_att = 0
    #     total_ch = 0

    #     for t in events[event]:
    #         if t == "Total":
    #             print(event)
    #             total_ch, total_att = events[event][t]
    #         else:
    #             c, a = events[event][t]
    #             g = a + c
    #             w_sheet.write(i, 0, t)
    #             w_sheet.write(i, 1, str(a))
    #             w_sheet.write(i, 2, str(c))
    #             w_sheet.write(i, 3, str(g))
    #             w_sheet.write(i, 4, str(100*(c/g)) + "%")
    #             i += 1
    #     w_sheet.write(i, 0, "Total")
    #     w_sheet.write(i, 1, str(total_att))
    #     w_sheet.write(i, 2, str(total_ch))
    #     w_sheet.write(i, 3, str(total_ch+total_att))
    #     w_sheet.write(i, 4, str(100*(total_ch/(total_att+total_ch))) + "%")
    #     i += 3



    # wb.save("Venue.xlsx")
    
