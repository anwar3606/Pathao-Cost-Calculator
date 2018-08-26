import mailbox
import csv
import re
import sys

counter = 0
total_counter = 0

with open('pathao_cost.csv', 'w', newline='') as mbox_file:
    fieldnames = ['Day', 'Date','Month', 'Cost', 'Pick-Up','Pick-Down', 'Rider', 'License-Number']
    pathao_output_csv = csv.DictWriter(mbox_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, fieldnames=fieldnames)
    # pathao_output_csv.writeheader()

    for message in mailbox.mbox(sys.argv[1]):
        total_counter += 1
        if message["from"] == '"Pathao Ride" <no-reply@pathao.com>':
            counter += 1
            print("Parsing: "+str(total_counter)+" Found: " +str(counter), end='\r')
            amount  = re.search(
                r'Tk. (\d+(\.?\d+)?)', message._payload, re.IGNORECASE)
            time  = message['Date'].split(' ')
            day  = time[0].replace(',', '')
            date  = time[1]
            month  = time[2]
            pickup  = re.search(
                r'"pick-up-location".*?</span>(.*?)<.*?/td>', message._payload, re.DOTALL)
            pickdown  = re.search(
                r'"pick-down-location".*?</span>(.*?)<.*?/td>', message._payload, re.DOTALL)
            rider  = re.search(
                r'<strong style=3D\"color: #000000;\">(.*?)</td>', message._payload, re.DOTALL)
            rider, license_no  = re.compile(r'</strong> <br.*?/>').split(rider.group(1).replace('=\n', ''))
            pathao_output_csv.writerow({
                'Day': day, 
                'Date': date, 
                'Month': month, 
                'Cost': amount.group(1), 
                'Pick-Up': pickup.group(1).replace('\n', '').replace('=', ''), 
                'Pick-Down': pickdown.group(1).replace('\n', '').replace('=', ''),
                'Rider': rider.replace('=', ''),
                'License-Number': license_no.replace('=', ''),
                })
        else:
            print("Parsing: "+str(total_counter)+" Found: " +str(counter), end='\r')

print('\n')