import requests
import json
import pandas as pd
from bs4 import BeautifulSoup

#list of device ids of tuners in Domoticz 
tunerIDs = ['100','101','102']

tuners = requests.get('http://192.168.1.7/tuners.html')
pageHTML = tuners.text
soup = BeautifulSoup(pageHTML, 'lxml')
table = soup.find_all('table')[0]
channels = []
for row in table.find_all('tr'):
    #get tuner
    tdTuner = row.find_all('td')[0]
    tdTunerData = tdTuner.text
    tunerParts = tdTunerData.split(' ')
    tuner = tunerParts[1]
    #get channel
    tdChannel = row.find_all('td')[1]
    tdData = tdChannel.text
    channelParts = tdData.split(' ')
    channel = channelParts[0]
    if channel != "not":
        channels.append(channel)
    else:
        channels.append('none')
        
response = requests.get('http://api.hdhomerun.com/api/guide.php?DeviceAuth=wwDrXISfjLGOXsP7VuDQo82V')
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

titleNumber = 0
for device in tunerIDs:
    
    if channels[titleNumber] != 'none':
        renameDevice = 'http://192.168.1.2:8080/json.htm?type=setused&idx=' + device + '&name=HDHomerun Tuner ' + str(titleNumber) + ' - Channel ' + channels[titleNumber] + '&used=true'
        results = requests.get(renameDevice)
        url = 'http://192.168.1.2:8080/json.htm?type=command&param=udevice&idx=' + device + '&nvalue=1&svalue=' + channels[titleNumber] + ' - ' + titles[titleNumber] + ''
        result = requests.get(url)
        #print(result.text)
        #print(url)
        titleNumber += 1
    else:
        renameDevice = 'http://192.168.1.2:8080/json.htm?type=setused&idx=' + device + '&name=HDHomerun Tuner ' + str(titleNumber) + ' - Not in Use&used=true'
        results = requests.get(renameDevice)
        url = 'http://192.168.1.2:8080/json.htm?type=command&param=udevice&idx=' + device + '&nvalue=0&svalue=' + titles[titleNumber]
        result = requests.get(url)
        #print(result.text)
        #print(url)
        titleNumber += 1

