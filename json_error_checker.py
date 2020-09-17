# -*- coding: utf-8 -*-
"""
Author: Scott Miller
PhD Candidate at Florida State University
Advisor: Andrew Rassweiler

This script was written for NSF project, "CNH-L: Multiscale Dynamics of Coral Reef Fisheries: Feedbacks Between Fishing Practices, Livelihood Strategies, and Shifting Dominance of Coral and Algae" (Award #1714704).

This script checks the exported JSON generated from coralnet_api_deployer.py for errors.  If no errors are detected, then it prints "No errors!" and completes quickly.  If errors
are detected, it will then attempt to fix the errors by sending new post/get requests to CoralNet and overwriting the error entries with data.  If it successfully
fixes all errors, it will print "A-OK!" when completed and the final script, json_parser.py, can be run.  Otherwise, it will print "STILL HAVE ISSUES!!!!" and you 
can either try running it again to fix these or you may have other issues.
"""

#Imports required libraries
import requests
import json
import re
import dropbox
import random
import time
import os

#Defining variables to locate the relevant files
site_to_use = '' #Same name as in previous script
local_path = '' #Pathway leading up to where these files will be saved on your local drive
image_extension = '' #The file extension (without the preceding period) for you uploaded images.  In my case, I use JPEGs, so this value is "JPG"
dropbox_token = '' #Your Dropbox token
dropbox_path = '' #This variable is the pathway leading to the folder you want to search for on Dropbox (ex, I have my folder_to_use inside a folder called "CoralNet", so this would be "/CoralNet/")

#Defining variables used to interface with CoralNet
classifier_url = '' #The URL of the CoralNet source you are using to annotate your images
coralnet_token = '' #Your CoralNet authorization token

#Sets up headers in case we need to send more requests to CoralNet to fix errors
headers = {"Authorization": f"Token {coralnet_token}", 
               "Content-type": "application/vnd.api+json"}

#Connects to our Dropbox account
dbx = dropbox.Dropbox(dropbox_token)
dbx.users_get_current_account()

#This script takes the newly-generated json file from coralnet_api_deployer.py, checks for errors, and attempts to correct those errors

#Opens the new file
f = open(f"{local_path}{site_to_use}_export.json",)

#Converts the json file into a dictionary and extracts the value from the only key
dat = json.load(f)
d = dat['data']

#Checks for images that returned errors instead of data for points
#If it finds any, it generates a new json file for these images that can be added to 
error_images = []
error_index = []
error_dat = {"data":[]}

for i in range(len(d)):

    attrib = d[i]['attributes']
    
    if 'error' in attrib.keys(): #Checks to see if the 'error' key is in the image attribute dictionary
            error_images.append(re.search(f'^.*[/](.*[.{image_extension}])', d[i]['id']).group(1)) #If it is, it adds the image name to the error_images list
            error_index.append(i) #And it saves the index to be removed later

if len(error_images) > 0:
    
    #Now that we know which elements are errors, we want to remove these from the lists so they can be replaced
    for ele in sorted(error_index, reverse = True):
        del dat['data'][ele] #Deletes the entries from the shorter list we're working with and from the larger json
    
    #Now, we take the images that threw errors and generate a new json file for them
    error_dat = {"data":[]}
    
    for entry in error_images:
        pathway = f'{dropbox_path}{site_to_use}/' + entry
        tmp_name = dbx.sharing_create_shared_link(path = pathway, short_url=False, pending_upload=None)
        
        to_append = {"type": "image", 
                    "attributes":{"url":tmp_name.url[:-1] + '1', 
                                  "points":[
                                          {"row": random.randint(450, 870), 
                                          "column": random.randint(600,1067)}, 
                                          {"row": random.randint(450,870), 
                                           "column": random.randint(1067,1533)},
                                          {"row": random.randint(450,870), 
                                           "column": random.randint(1533,2000)},
                                          {"row": random.randint(450,870), 
                                           "column": random.randint(2000,2467)},
                                          {"row": random.randint(450,870), 
                                           "column": random.randint(2467,2933)},
                                          {"row": random.randint(450,870), 
                                           "column": random.randint(2933,3400)},
                                          {"row": random.randint(870,1290), 
                                          "column": random.randint(600,1067)}, 
                                          {"row": random.randint(870,1290), 
                                           "column": random.randint(1067,1533)},
                                          {"row": random.randint(870,1290), 
                                           "column": random.randint(1533,2000)},
                                          {"row": random.randint(870,1290), 
                                           "column": random.randint(2000,2467)},
                                          {"row": random.randint(870,1290), 
                                           "column": random.randint(2467,2933)},
                                          {"row": random.randint(870,1290), 
                                           "column": random.randint(2933,3400)},
                                          {"row": random.randint(1290,1710), 
                                          "column": random.randint(600,1067)}, 
                                          {"row": random.randint(1290,1710), 
                                           "column": random.randint(1067,1533)},
                                          {"row": random.randint(1290,1710), 
                                           "column": random.randint(1533,2000)},
                                          {"row": random.randint(1290,1710), 
                                           "column": random.randint(2000,2467)},
                                          {"row": random.randint(1290,1710), 
                                           "column": random.randint(2467,2933)},
                                          {"row": random.randint(1290,1710), 
                                           "column": random.randint(2933,3400)},
                                          {"row": random.randint(1710,2130), 
                                           "column": random.randint(600,1067)},
                                          {"row": random.randint(1710,2130), 
                                           "column": random.randint(1067,1533)},
                                          {"row": random.randint(1710,2130), 
                                           "column": random.randint(1533,2000)},
                                          {"row": random.randint(1710,2130), 
                                           "column": random.randint(2000,2467)},
                                          {"row": random.randint(1710,2130), 
                                           "column": random.randint(2467,2933)},
                                          {"row": random.randint(1710,2130), 
                                           "column": random.randint(2933,3400)},
                                          {"row": random.randint(2130,2550), 
                                           "column": random.randint(600,1067)},
                                          {"row": random.randint(2130,2550), 
                                           "column": random.randint(1067,1533)},
                                          {"row": random.randint(2130,2550), 
                                           "column": random.randint(1533,2000)},
                                          {"row": random.randint(2130,2550), 
                                           "column": random.randint(2000,2467)},
                                          {"row": random.randint(2130,2550), 
                                           "column": random.randint(2467,2933)},
                                          {"row": random.randint(2130,2550), 
                                           "column": random.randint(2933,3400)},
                                          ]
                                      }
                                  }
        error_dat['data'].append(to_append)
        
    #Now that we have identified error images, deleted them from the master json structure, and created a new json for them
    #We need to query coralnet again to attempt to get actual data from them
   
    k = 0
    dat_length = 100
    export = {"data":[]}
    
    while dat_length == 100:
        
        error_data = {"data":error_dat['data'][k:k+100]}
        dat_length = len(error_data['data'])
    
        if dat_length == 0:
            break
        
        #This writes the error json to a file so it can be used by the coralnet post request
        with open(f'{local_path}error_json.json', 'w') as outfile:
            json.dump(error_data, outfile)
        
    #Sends the initial post request to coralnet
        r = requests.post(url=classifier_url, data=open(f"{local_path}error_json.json"), headers=headers)
    
        time.sleep(60)    
        in_progress = True
            
        while in_progress: #This pings CoralNet every 60 seconds to check the status of the job
                
            r_status = requests.get(url = 'https://coralnet.ucsd.edu'+r.headers['Location'], headers = {"Authorization": f"Token {coralnet_token}"})
                
            curr_status = json.loads(r_status.content) #Extracts the content from the json request
                
            if 'status' in curr_status['data'][0]['attributes'].keys(): #Checks to see if the status key is in the request dictionary - if not it is complete
                print(curr_status['data'][0]['attributes']['successes'])
                time.sleep(60) #Waits 60s before attempting the next status update
                
            else: #If it doesn't find 'status' key, then it sets in_progress to false and saves the request data
                export['data'].extend(curr_status['data'])
                in_progress = False
                
        k += 100
        
    #Now checks the new data from coralnet for new errors
    #If it finds any, it alerts the user that there's STILL issues
    #Otherwise, it adds the new data to the old json, and exports a new file with all the data to be parsed by json_parser
    exp_dat = export['data']
        
    error_images = []
    error_index = []
    error_dat = {"data":[]}
        
    for i in range(len(exp_dat)):
        
        attrib = exp_dat[i]['attributes']
            
        if 'error' in attrib.keys(): #Checks to see if the 'error' key is in the image attribute dictionary
            error_images.append(re.search(f'^.*[/](.*[.{image_extension}])', d[i]['id']).group(1)) #If it is, it adds the image name to the error_images list
            error_index.append(i) #And it saves the index to be removed later
                    
    if len(error_images) > 0:
        print('STILL HAVE ISSUES!!!!')
    else:
        dat['data'].extend(exp_dat)
        print('A-OK!')
        
        #Now, we export the error-checked file!
        with open(f'{local_path}{site_to_use}_export.json', 'w') as outfile:
            json.dump(dat, outfile)
            
        #...and we delete the error_json.json file
        del r
        os.remove(f'{local_path}error_json.json')

else:
    print('No errors!')
