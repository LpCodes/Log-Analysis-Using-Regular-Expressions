#!/usr/bin/env python3
import csv
import re
import operator

# data = open("syslog.log", "r")  # open file

# create req dict
messages_count = {}
user_data = {}

with open("syslog.log", "r") as file:
    for line in file.readlines():
        # print(line)
        m1 = re.search(r"ticky:\s*.*?\s*([\w '?]+)", line)  # for error msg
        if m1 is None:
            continue

        # adding error if not in dic & iter if prest
        if m1.group(1) not in messages_count:
            messages_count[m1.group(1)] = 1
        else:
            messages_count[m1.group(1)] += 1

        m1 = re.search(r"ticky:\s*.*\s*([\w '?]+)\s*\((\w+)\)", line)
        Err = re.search(r"ticky:\s*ERROR\s*([\w '?]+)\s*\((\w+)\)", line)
        inf = re.search(r"ticky:\s*INFO\s*([\w '?]+)\s*(\w+)", line)
        # print(Err)
        # print(inf)
        if m1 is None:
            continue
        if m1.group(2) not in user_data.keys():  # creating user with default values as 0
            user_data[m1.group(2)] = {}
            user_data[m1.group(2)]['INFO'] = 0
            user_data[m1.group(2)]['ERROR'] = 0

        # adding val to dict as  much found
        if Err is not None:
            user_data[m1.group(2)]['ERROR'] += 1
        if inf is not None:
            user_data[m1.group(2)]['INFO'] += 1

# print(messages_count)
# sorting ops
sorted_error_list = sorted(messages_count.items(),
                           key=operator.itemgetter(1), reverse=True)

sorted_user_data = sorted(user_data.items(), key=operator.itemgetter(0))

# print(sorted_error_list)

# data.close()  # close file

# print(sorted_error_list)
# print(sorted_user_data)

# for x, k in sorted_error_list:
#     print(x, k)

# * Create CSV file error_messages
with open('error_message.csv', 'w') as fileObj:
    # Create a CSV writer object
    writerObj = csv.writer(fileObj)
    # Add header row as the list
    writerObj.writerow(["Error Message", "Count"])  # write col name in list
    for x in sorted_error_list:
        # Append the list as a row to the csv file
        writerObj.writerow(x)

# * Create CSV file user_statistics
with open('user_statistics.csv', 'w', ) as user_csv:
    # Create a CSV writer object
    writerObj = csv.writer(user_csv)
    # Add header row as the list
    writerObj.writerow(["Username", "Info", "Error"])
    for x, k in sorted_user_data:
        # Append the list as a row to the csv file
        # print(x, k["INFO"], k["ERROR"])
        writerObj.writerow([x, k["INFO"], k["ERROR"]])
