# -*- coding: utf-8 -*-
"""
Author: Scott Miller
PhD Candidate at Florida State University
Advisor: Andrew Rassweiler

This script was written for NSF project, "CNH-L: Multiscale Dynamics of Coral Reef Fisheries: Feedbacks Between Fishing Practices, Livelihood Strategies, and Shifting Dominance of Coral and Algae" (Award #1714704).

This script locates your images stored on a Dropbox account and generates a JSON file that will be sent to the CoralNet API to tell it which images to annotate and where 
to place points to score.  It is set up for the purposes of our research project which places 30 stratified random points on 4000x3000 images, excluding the outer 15% 
of the image.  You will likely need to change the to_append section to generate points that make sense for your particular project, but hopefully this provides a good 
jumping off point.
"""
#Imports necessary libraries
import dropbox
import json
import random

#Defines variables
folder_to_use = '' #This variable is the folder you want to search for on Dropbox and will also be how the resulting JSON will be named
local_path = '' #This is the pathway on you local machine where these files will be saved and located (ex, for me it is "C:\\Users\\sdmiller\\Documents\\CoralNet\\" -- note the double slashes)
dropbox_path = '' #This variable is the pathway leading to the folder you want to search for on Dropbox (ex, I have my folder_to_use inside a folder called "CoralNet", so this would be "/CoralNet/")

dropbox_token = '' #This is the authorization token for your Dropbox account

#Connects to our Dropbox account
dbx = dropbox.Dropbox(dropbox_token)
dbx.users_get_current_account()

#Creates empty list to store the file names within the folder of interest
file_list = []

#Pulls out first 2000 files from the folder, adds the names to file_list, then creates a cursor 
#signifying its end location in the folder
file_list_all = dbx.files_list_folder(f'{dropbox_path}{folder_to_use}')
file_list.extend(file_list_all.entries)
file_cursor = file_list_all.cursor

keep_retrieving = True #Sets this as True, and will change to False when all files retrieved
while keep_retrieving: #Loops through to retrieve the rest of the images
    file_list_continue = dbx.files_list_folder_continue(file_cursor)
    file_list.extend(file_list_continue.entries)
    file_cursor = file_list_continue.cursor
    
    if len(file_list_continue.entries) == 0:
        keep_retrieving = False

dat = {"data":[]}

'''
#This block can be uncommented to generate the list of file names from Dropbox
#Can be used to check which images didn't upload in the case of errors during the upload process
file_dict = {}
k = 1
for entry in file_list:
    file_dict[f'row_{k}'] = entry.name
    k += 1
    
import pandas as pd
file_list = pd.DataFrame.from_dict(file_dict, orient = 'index')
file_list.to_csv(f'{local_path}{folder_to_use}_file_list.csv', index=False)
'''
for entry in file_list:
    pathway = f'{dropbox_path}{folder_to_use}/' + entry.name
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
                                      "column": random.randint(600,1710)}, 
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
    dat['data'].append(to_append)

with open(f'{local_path}{folder_to_use}.json', 'w') as outfile:
    json.dump(dat, outfile)
