import requests
import os
from os import path
import json
import urllib.request
from PIL import Image
import shutil
from shutil import make_archive
import time

#set varibles
channels = []
dirName = "HDHomerunIcons"
#Sizes to resize icon to
size48 = 48,48
size14 = 14,14

#function to download icons from HDHomerun
def downloader(image_url, channel):
    file_name = channel
    full_file_name = dirName + '/' + channel + '/' + str(file_name) + 'Channel48_On.png'
    tiny = dirName + '/' + channel + '/' + str(file_name) + 'Channel.png'
    channelPath = dirName + '/' + channel 
       
    if path.exists(dirName + '/' + file_name):
        print('Already have image for Channel')

    else:

        os.mkdir(channelPath)
        urllib.request.urlretrieve(image_url,full_file_name)
        print('Downloaded ' + image_url + ' : ' + full_file_name)
        big = Image.open(full_file_name)
        big.thumbnail(size48,Image.ANTIALIAS)
        big.save(full_file_name, "png")

        small = Image.open(full_file_name)
        small.thumbnail(size14,Image.ANTIALIAS)
        small.save(tiny, "png")
        #shutil.copy(full_file_name, dirName + '/' + channel + '/' + str(file_name) + 'Channel48_Off.png')

        #Make a copy of icon images in www/images directory
        print("Moving images to www/images directory")
        shutil.copyfile(tiny, '../../www/images/' + channel + 'Channel.png')
        shutil.copyfile(full_file_name, '../../www/images/' + channel + 'Channel48_On.png')
        shutil.copyfile(full_file_name, '../../www/images/' + channel + 'Channel48_Off.png')
        #print('______________________________________________________')
    
        
        #Updat switch_icons.txt file
        f = open('../../www/switch_icons.txt', 'a')
        f.write('\n' + channel + 'Channel;' + channel + 'Channel;' + channel + ' Channel Logo')
        f.close()

        print('Channel Information:')
        print('Base: ' + channel)
        base = channel + 'Channel'
        print('Name: ' + channel)
        name = channel + ' Channel'
        print('Description: ' + channel + 'Logo')
        description = 'Channel ' + channel + ' Logo'
        print('IconSmall Path: ' + dirName + '/' + channel + '/' + channel + 'Channel.png')
        iconSmall = dirName + '/' + channel + '/' + channel + 'Channel.png'
        print('IconOn Path: ' + dirName + '/' + channel + '/' + channel + 'Channel48_On.png')
        iconOn = dirName + '/' + channel + '/' + channel + 'Channel48_On.png'
        print('IconOff Path: ' + dirName + '/' + channel + '/' + channel + 'Channel48_Off.png')
        iconOff = dirName + '/' + channel + '/' + channel + 'Channel48_Off.png'
        channels.append(channel)

#Begin script
#Check to see if image data had already been downloaded 

if not os.path.exists(dirName):
    os.mkdir(dirName)
    print("Directory " , dirName ,  " Created ")
else:    
    print("Directory " , dirName ,  " Already Exists")


#Get the authResponse from HDHomerun device
authResponse = requests.get('http://192.168.1.7/discover.json')
adata = authResponse.json()
DeviceAuth = adata['DeviceAuth']
print(DeviceAuth)

#Get channel images from guide information from HDHomerun device
response = requests.get('http://api.hdhomerun.com/api/guide.php?DeviceAuth=' + DeviceAuth)
jdata = response.json()

#loop through jason data to  find image URLs
for i in jdata:
    if "ImageURL" in i:
        imageLink = (i['ImageURL'])
        channelNum = (i['GuideNumber'])
        downloader(imageLink, channelNum)
    else:
        imageLink = 'http://192.168.1.2:8080/images/TV48_On.png'
        channelNum = (i['GuideNumber'])
        downloader(imageLink, channelNum)



           



        
        
    

