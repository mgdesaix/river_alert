#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 23:32:00 2017

@author: mdesaix

This checks every 6 hours to see if the Lower James is above 4 feet in the river forecast
If it is, it emails me the river information
"""


import requests
from bs4 import BeautifulSoup
from dateutil import tz
from datetime import datetime
import smtplib
import time

while True:

    url = "https://water.weather.gov/ahps2/hydrograph_to_xml.php?gage=rmdv2&output=xml"
    headers = {'content-type': 'text'}
    response = requests.get(url, headers)
    soup = BeautifulSoup(response.text, "lxml")
    
    def river_alert(soup):
        forecast = soup.find('forecast')
        forecast_stage = forecast.find_all('primary')
        high =[]
        for stage in forecast_stage:
            stage_float = float(stage.text)
            high_stage = stage_float > 4
            high.append(high_stage)
        any_high = any(high)
        return any_high
    
    if river_alert(soup) == False:
        # sleep for 6 hours or 21600 seconds
        time.sleep(21600)
        continue
    else:
    
    
        def get_river_info(soup):
            forecast = soup.find('forecast')
            
            date_string = forecast.find_all('valid')
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
                
                # river height
                height = str(datum.primary.text)
                row.append(height)
                # flow
                flow = str(datum.secondary.text)
                row.append(flow)
                river_info.append(row)
            return river_info
        river_info = get_river_info(url, headers)
        
        name = soup.site['name']
        
        subject = 'Subject: THE RIVER IS OR (WILL BE) OVER 4 FT!!!!\n'
        message = name + '\n'
        for row in river_info:
            flow_int = 1000 * float(row[2])
            message += '\nTime: ' + str(row[0])
            message += '\nHeight: ' + row[1] + ' feet'
            message += '\nFlow: ' + str(flow_int) + ' cfs'
            message += '\n'
            
        
        
        msg = subject + message
        
        # email from myself to both email addresses
        fromaddr = 'mgdesaix@gmail.com'
        toaddrs = ['mgdesaix@gmail.com', 'desaixmg@mymail.vcu.edu']
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        # login name and password
        server.login('mgdesaix@gmail.com', 'email_password')
        # make sure to change gmail privacy app settings
        
        # send the email
        server.sendmail(fromaddr, toaddrs, msg)
        server.quit()
        
        break
