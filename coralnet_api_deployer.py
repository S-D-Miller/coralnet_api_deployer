# -*- coding: utf-8 -*-
"""
Author: Scott Miller
PhD Candidate at Florida State University
Advisor: Andrew Rassweiler

This script was written for NSF project, "CNH-L: Multiscale Dynamics of Coral Reef Fisheries: Feedbacks Between Fishing Practices, Livelihood Strategies, and Shifting Dominance of Coral and Algae" (Award #1714704).

This script queries the CoralNet API to automatically score images based on the JSON file generated using "json_generator.py".  Currently, the API can only accept requests of 
100 images, so this breaks up the JSON file into 100 image chunks, sends these to the API, checks every 60s on the status of them, saves the annotations when complete, then sends
the next 100 images.  It prints status updates to the console so you can track its progress.
"""

#Imports required packages
import requests
import json
import time
import os

#Defining variables to locate the relevant files
site_to_use = '' #This variable is the folder you want to search for on Dropbox and will also be how the resulting JSON will be named (same as "folder_to_use" in json_generator.py)
local_path = '' #Pathway that your file is saved

#Defining variables used to interface with CoralNet
classifier_url = '' #The URL of the source used to annotate images
coralnet_token = '' #Your CoralNet authorization token

#Opens the JSON file created by json_generator.py
with open(f"{local_path}{site_to_use}.json", "r") as f:
      d = json.load(f)

#Saves the classifier URL you will be using and your CoralNet authorization token
headers = {"Authorization": f"Token {coralnet_token}", 
           "Content-type": "application/vnd.api+json"}

#Sets up some variables that will be used in the deployment loop
k = 0 #k is a variable that is initialized at 0 and increases by 100 each loop iteration.  It is used to move along the larger JSON file and mark which images to pull out.
dat_length = 100 #Initialized at 100, but will change based on how many photos are pulled for each value of k
export = {"data":[]} #Sets an empty dictionary that will store the resulting data

#This is the loop that is used to send the many requests to the API.  It will continue until k gets large enough that it will exceed the number of images in the JSON file.
while dat_length == 100:
    
    #Pulls out the 100 images 
    dat = {"data":d['data'][k:k+100]} 
    dat_length = len(dat['data'])
    
    if dat_length == 0:
        break
    #Prints k so you can monitor progress in the console
    print(f'K = {k}') 
    
    #Writes a temporary JSON file in the same directory as the larger file containing the images pulled out earlier.
    with open(f'{local_path}temp_json.json', 'w') as outfile:
        json.dump(dat, outfile)

    #Sends the post request to the CoralNet API using the temp JSON file and the headers defined earlier
    r = requests.post(url=classifier_url, data=open(f"{local_path}temp_json.json"), headers=headers)

    time.sleep(60) #Waits 60 seconds before attempting to retrieve results from the post request    
    in_progress = True
    
    while in_progress: #This pings CoralNet every 60 seconds to check the status of the job
        
        #Sends a get request in an attempt to retrieve the annotations
        r_status = requests.get(url = 'https://coralnet.ucsd.edu'+r.headers['Location'], headers = {"Authorization": f"Token {coralnet_token}"})
        
        curr_status = json.loads(r_status.content) #Extracts the content from the json request
        
        if 'status' in curr_status['data'][0]['attributes'].keys(): #Checks to see if the status key is in the request dictionary - if not it is complete
            print(curr_status['data'][0]['attributes']['successes'])
            time.sleep(60) #Waits 60s before attempting the next status update
        
        else: #If it doesn't find 'status' key, then it sets in_progress to false and saves the request data
            export['data'].extend(curr_status['data'])
            in_progress = False
            
    #Creates a temp json with the data in case Python crashes -- this provides a way to upload later and avoid losing all the time
    with open(f'{local_path}export_temp.json', 'w') as outfile:
        json.dump(export, outfile)
        
    k += 100 #Increases k by 100 to allow it to pull the next 100 images (or end the script if it has already pulled all the images)
    
#Creates a final json file with the relevant information included
with open(f'{local_path}{site_to_use}_export.json', 'w') as outfile:
      json.dump(export, outfile)

#Removes the two temp json files because they are not needed anymore as the script has completed
del r #Deletes the request variable to unlock the temp_json file so it can be deleted
os.remove(f'{local_path}temp_json.json')
os.remove(f'{local_path}export_temp.json')
