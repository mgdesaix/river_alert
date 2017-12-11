#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 20:41:18 2017
@author: mdesaix
This provides time, stage, and flow data for the Lower James River on the westham gage.  Run the script, email is sent.
"""
import requests
from bs4 import BeautifulSoup
from dateutil import tz
from datetime import datetime
import smtplib

url = "https://water.weather.gov/ahps2/hydrograph_to_xml.php?gage=rmdv2"
response = requests.get(url)
soup = BeautifulSoup(response.text, "xml")
def get_river_info(soup):
    forecast = soup.find('forecast')
    # 'valid' is the tag for date/time, I just want the first 4 instances
    date_string = forecast.find_all('valid')[0:4]
    river_info =[]
    for item in date_string:
        row = []
        datum = item.find_parent('datum') 
        #Date/time
        #set zones: the river gage data uses UTC, the to_zone is set as local
        from_zone = tz.gettz('UTC')
        to_zone = tz.tzlocal()
        # Find the date/time from river data
        date_and_time = datum.valid.text[0:19]
        # specify format
        utc = datetime.strptime(date_and_time, '%Y-%m-%dT%H:%M:%S')
        # specify zone
        utc = utc.replace(tzinfo=from_zone)
        local_time = utc.astimezone(to_zone)
        row.append(local_time)
        # river height/stage, specified by 'primary' tag
        height = str(datum.primary.text)
        row.append(height)
        # flow, specified by 'secondary'tag
        flow = str(datum.secondary.text)
        row.append(flow)
        river_info.append(row)
    return river_info
river_info = get_river_info(soup)

name = soup.site['name']

subject = 'Subject: River information for %s\n' % name
message = name + '\n'
for row in river_info:
    # convert kcfs to cfs...cause
    flow_int = 1000 * float(row[2])
    message += '\nTime: ' + str(row[0])
    message += '\nHeight: ' + row[1] + ' feet'
    message += '\nFlow: ' + str(flow_int) + ' cfs'
    message += '\n'
    
msg = subject + message

# email from myself to both email addresses
fromaddr = 'mgdesaix@gmail.com'
toaddrs = ['mgdesaix@gmail.com', 'desaixmg@mymail.vcu.edu']
# If I was to actually run this I would uncomment these:
# server = smtplib.SMTP('smtp.gmail.com', 587)
# server.starttls()
# server.login('mgdesaix@gmail.com', 'email_password')

# make sure to change gmail privacy app settings
# print email's contents
print('From: ' + fromaddr)
print('To: ' + str(toaddrs))
print('Message: ' + msg)
# uncomment these:
# send the email
# server.sendmail(fromaddr, toaddrs, msg)
# server.quit()
