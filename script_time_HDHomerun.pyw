#!/usr/bin/env python3.6

"""
#################################################################

Script writen by moengiant
Last Uodated: 4/29/20

**** Important ****

Need to run the HDHomerunIconsSimple.py before using this script
as that script add channel icons to the www/iamges directory
and edits the switch_icons.txt file

#################################################################
"""

import requests
import urllib
from urllib.parse import urlencode
import urllib.request
import json
from bs4 import BeautifulSoup

# list of device ids of tuners in Domoticz 
# edit this list to match the idx numbers of the devices set up in domoticz 
tunerIDs = ['100','101','102']
# edit this path to the absolute path to the switch_icons.txt file 
pathSwitchIcons = "C:/Program Files (x86)/Domoticz/www/switch_icons.txt"
# edit the ip to match the ip of the HDHomerun device
ipHD = "0.0.0.0"
# edit the ip to match the ip of the Domoticz server
ipDS = "0.0.0.0"
# edit the port to match the port of the Domoticz server
portDS = "8080"

#################################################################
#                  DO NOT EDIT BELOW THIS LINE                  #
#################################################################

def hunter(needle):
    # loop through switch_icons.txt to find matching line
    # edit this path absolute to the absolute path in domotics
        myFile = open(pathSwitchIcons,"r")
        custImage = 0
        for line in myFile:
            # found a match 
            if line.strip() == needle:
                return(custImage)
                break
            custImage += 1
    
# scrape turner channel data
tuners = requests.get('http://' + ipHD + '/tuners.html')
pageHTML = tuners.text
soup = BeautifulSoup(pageHTML, 'lxml')
table = soup.find_all('table')[0]
channels = []
for row in table.find_all('tr'):
    # get tuner
    tdTuner = row.find_all('td')[0]
    tdTunerData = tdTuner.text
    tunerParts = tdTunerData.split(' ')
    tuner = tunerParts[1]
    # get channel
    tdChannel = row.find_all('td')[1]
    tdData = tdChannel.text
    channelParts = tdData.split(' ')
    channel = channelParts[0]
    if channel != "not":
        channels.append(channel)
    else:
        channels.append('none')

# get the authResponse from HDHomerun device
authResponse = requests.get('http://' + ipHD + '/discover.json')
adata = authResponse.json()
DeviceAuth = adata['DeviceAuth']
log = "http://" + ipDS + ":" + portDS + "/json.htm?type=command&param=addlogmessage&message=1)+Fetching HDHomerun Key: " + DeviceAuth
req = requests.get(log)
        
# get guide from HDHomerun device
response = requests.get('http://api.hdhomerun.com/api/guide.php?DeviceAuth=' + DeviceAuth)
jdata = response.json()
titles = []
#stations = []
for channel in channels:
    if channel != 'none':
        for i in jdata:
            if i['GuideNumber'] == channel:
                #station = (i['Affiliate'])
                #stations.append[station]
                title = (i['Guide'][0]['Title'])
                titles.append(title)
                break
    else:
        titles.append('Tuner Not in Use')


#Update Domoticz devices with HDHomerun data
# step through tunerIDs array
titleNumber = 0
log = "http://" + ipDS + ":" + portDS + "/json.htm?type=command&param=addlogmessage&message=2)+Checking+" + str(len(titles)) + "+HDHomerun+Tuners"
req = requests.get(log)

for device in tunerIDs:

    url = ''
    params = ''
    channelNum = str(channels[titleNumber])
    
    if channelNum != 'none':
        # Tuner is set to  a channel number
        log = "http://" + ipDS + ":" + portDS + "/json.htm?type=command&param=addlogmessage&message=3)+Tuner+" + str(titleNumber) + "+set+to+channel+" + str(channels[titleNumber])
        req = requests.get(log)

        # the string to find in the switch_icons.txt file
        # the line number of the string is the switch icon id number 
        lookup = str(channels[titleNumber]) + "Channel;" + str(channels[titleNumber]) + "Channel;" + str(channels[titleNumber]) + " Channel Logo"
        line = ''

        custImage = hunter(lookup)
        message = str(custImage)
        
        
        log = "http://" + ipDS + ":" + portDS + "/json.htm?type=command&param=addlogmessage&message=4)+Found+switch+icon+id:+" + str(custImage)
        req = requests.get(log)
                                                                                                                                  
        # set url and header
        url = "http://" + ipDS + ":" + portDS + "/json.htm?"

        # update device name and image
        params = urlencode({'type':'setused','used':'true','idx':'' + str(device) + '','switchtype':'0','name': 'HDHomerun Tuner ' + str(titleNumber) + ' - Channel ' + str(channels[titleNumber]) + '','customimage': '' + str(custImage) + ''})
        #print(params)
        path = url + params
        response = urllib.request.urlopen(path)
        
        
        # turn device on
        params = urlencode({'type':'command','param':'udevice','idx':'' + device + '','nvalue':'1','svalue':'1'})
        #print(params)
        path = url + params
        response = urllib.request.urlopen(path)
        
        # update log
        params = urlencode({'type':'command','param':'addlogmessage','message':'5) Setting device idx ' + str(device) + ' name to ' + str(channels[titleNumber]) + ' and changing switch icon id to ' + str(custImage) + ''})
        #print(params)
        path = url + params
        #response = urllib.request.urlopen(path)
        req = requests.get(path)

        titleNumber += 1
        
    else:

        # set url and header
        url = "http://" + ipDS + ":" + portDS + "/json.htm?"

        #update device name
        params = urlencode({'type':'setused','used':'true','idx':'' + device + '','switchtype':'0','name':'HDHomerun Tuner ' + str(titleNumber) + ' - Not in Use','customimage':'2'})
        path = url + params
        response = urllib.request.urlopen(path)
        
        
        # turn off device
        params = urlencode({'type':'command','param':'udevice','idx':'' + device + '','nvalue':'0','svalue':'0'})
        path = url + params
        response = urllib.request.urlopen(path)
        
        # update log
        params = urlencode({'type':'command','param':'addlogmessage','message':'Tuner ' + device + ' not in use'})
        path = url + params
        response = urllib.request.urlopen(path)
        
        titleNumber += 1
        
