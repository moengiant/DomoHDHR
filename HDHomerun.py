import requests
import json
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

#Get the authResponse from HDHomerun device
authResponse = requests.get('http://192.168.1.7/discover.json')
adata = authResponse.json()
DeviceAuth = adata['DeviceAuth']
print(DeviceAuth)
        
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
titleNumber = 0
for device in tunerIDs:
    
    if channels[titleNumber] != 'none':
        
        print(channels[titleNumber])
        # 549Channel;549Channel;549 Channel Logo
        lookup = channels[titleNumber] + 'Channel;' + channels[titleNumber] + 'Channel;' + channels[titleNumber] + ' Channel Logo'
        print('__________________________________')
        print(device, lookup)
        line = ''
        num = 0
        #Get CustomImage ID (row number in switch_icons.txt file) for tv channel
        with open('../../www/switch_icons.txt') as myFile:
            for num, line in enumerate(myFile, 1):
                #print(num, line)
                if line.strip() == lookup:
                    print ('Found Line: '+ str(num), line)
                    custImage = str(num - 1)

        #custImage = '2'
        renameDevice = 'http://192.168.1.2:8080/json.htm?type=setused&used=true&idx=' + device + '&switchtype=0&name=HDHomerun Tuner ' + str(titleNumber) + ' - Channel ' + channels[titleNumber] + '&customimage=' + custImage + ''
        print(renameDevice)
        results = requests.get(renameDevice)
        url = 'http://192.168.1.2:8080/json.htm?type=command&param=udevice&idx=' + device + '&nvalue=1&svalue=' + channels[titleNumber] + ' - ' + titles[titleNumber] + ''
        result = requests.get(url)
        #print(results.text)
        #print(result.text)
        titleNumber += 1
        print('__________________________________')
        
    else:
        print('__________________________________')
        
        renameDevice = 'http://192.168.1.2:8080/json.htm?type=setused&used=true&idx=' + device + '&switchtype=0&name=HDHomerun Tuner ' + str(titleNumber) + ' - Not in Use&customimage=2'
        results = requests.get(renameDevice)
        url = 'http://192.168.1.2:8080/json.htm?type=command&param=udevice&idx=' + device + '&nvalue=0&svalue=' + titles[titleNumber]
        result = requests.get(url)
        #print(results.text)
        #print(result.text)
        titleNumber += 1
        print('__________________________________')
        
