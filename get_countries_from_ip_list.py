import csv
import json
import datetime

from urllib2 import urlopen

from country_iso_code import *

with open('user.csv', 'rb') as f:
    f.next() #skip first line
    reader = csv.reader(f)
    raw_discourse_data = list(reader)

creation_date = [i[5] for i in raw_discourse_data]
ip_address = [i[17] for i in raw_discourse_data]



# Get number of new members per month
account_creation_date = [datetime.datetime.strptime(d, "%Y-%m-%d %H:%M:%S UTC") for d in filter(None,creation_date)]

community_expansion = {}

for d in account_creation_date:

    period = datetime.datetime.strftime(d ,'%Y-%m')

    if period in community_expansion:
        community_expansion[period] += 1
    else:
         community_expansion[period] = 1


member_countries = {}

# Get number of IP in the same country
i = 0

for ip in ip_address:
    i += 1

    url = 'http://ipinfo.io/'+ ip +'/json'

    try:
        response = urlopen('http://ipinfo.io/'+ ip +'/json')
        data = json.load(response)
    except:
        # Skip all error \o/
        print ip
        continue

    # Skip if there is no information about the country
    if 'country' not in data:
        continue

    country = data['country']

    if country in member_countries:
        member_countries[country] += 1
    else:
         member_countries[country] = 1

    print 'Retrieiving location in progress:', (float(i)/len(ip_address))*100, '%'

print 'Cleaning data'
# remove unknown country
if '' in member_countries:
    del member_countries['']

# Retrieve country name from the ISO
for ISO in ISO2COUNTRY:
    if ISO not in member_countries:
        continue
    country_name = ISO2COUNTRY[ISO]
    member_countries[country_name] = member_countries.pop(ISO)

members_by_continent = {}

# Associate continent
for country in member_countries:
    iso = COUNTRY2ISO[country]
    con = ISO2CONTINENTS[iso]

    if con in members_by_continent:
        members_by_continent[con] += member_countries[country]
    else:
         members_by_continent[con] = member_countries[country]


print 'Export results in members.csv file'

with open('members.csv', 'w') as f:
    f.write('Country, number of users\n')
    [f.write('{0},{1}\n'.format(key, value)) for key, value in member_countries.items()]
    f.write('\nContinent, number of users\n')
    [f.write('{0},{1}\n'.format(key, value)) for key, value in members_by_continent.items()]

print 'Done !'
