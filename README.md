# coralnet_api_deployer
Contains python scripts to interface with the CoralNet API
_______________________
Author: Scott Miller  
PhD Candidate at Florida State University  
Advisor: Andrew Rassweiler

This repository was created for NSF project, "CNH-L: Multiscale Dynamics of Coral Reef Fisheries: Feedbacks Between Fishing Practices, Livelihood Strategies, and Shifting Dominance of Coral and Algae" (Award #1714704).
_______________________
This repository contains four Python scripts that are run in succession to generate a JSON file for the API (json_generator.py), send the post/get requests (coralnet_api_deployer.py), check for errors (json_error_checker.py), then parse the resulting JSON into a .csv (json_parser.py).  Below is documentation for the four scripts, in the order they should be run.  These operate under the assumption that images are stored on Dropbox, separated by folders of up to ~10000 images, although more could likely work, too (in our case, they are separated based on site).  As written, these use Python's f-string formatting, so they depend on using Python 3.6 or higher.  Version 10.4.1 of the dropbox module was used, so if you experience any issues with this module (particularly newer versions), please try using this version.

[Jordan Pierce](https://github.com/JordanMakesMaps) wrote a more in-depth tutorial and refined some of the code used here, so feel free to check out [his tutorial](https://github.com/JordanMakesMaps/CoralNet-API) for additional reference.

## 1. json_generator.py

  VARIABLES TO DEFINE:
  - folder_to_use --> Folder name that your images are stored in that you want scored (for us, these are sites, so an example is "16_Avaiti")
  - local_path --> Pathway leading to where you want the JSON files to be saved and subsequently read from (Ex, "C:\\Users\\sdmiller\\Documents\\CoralNet\\" is what I use)
  - dropbox_path -->  Pathway on Dropbox leading to the location of your "folder_to_use" (I have my folders inside a folder named CoralNet, so this value for me is: "/CoralNet/")
  - dropbox_token --> String of your Dropbox authorization token
  
  This script generates the JSON file that will be used to interface with the CoralNet API.  This JSON file generates 30 stratified random points across 4000x3000 pixel images, taken only from the inner 85% of the image.  It will do this for every image stored within the folder.  You can change the values where the points are generated to fit your own research purposes.  It generates a JSON file named {folder_to_use}.json in the {local_path} directory.

## 2. coralnet_api_deployer.py

  VARIABLES TO DEFINE:
  - site_to_use --> keep the same as "folder_to_use" from the json_generator.py script.
  - local_path --> Pathway leading to where your JSON is saved from json_generatory.py.  If you keep it the same as in that script, it will work without any intervention.
  - classifier_url --> The URL of the source used to annotate your images.
  - coralnet_token --> A string containing your CoralNet authorization token.  Make sure you have access to the CoralNet source you want to use.
  
    This script takes the JSON file generated with json_generator.py and uses it to send requests to the CoralNet API.  Currently, the API only allows requests of up to 100 images, so this breaks down the previous JSON (if greater than 100 images) into smaller segments to send to the API.  For every 100 images it sends the post request, then sends get requests (to retrieve the data) every 60 seconds.  If CoralNet is still working on images, it waits another 60 seconds and sends another get request until it has scored all images.  It prints the k value (the maximum number of total requests sent so far, in 100 increments) as well as the images scored in each get request (up to 100) so you can monitor its status.  While this script is running, it creates two temporary JSON files in the local_path directory.  The first, temp_json.json is used by the script to send the post request, and is overwritten every iteration of the main loop.  The other is temp_export.json, which creates a running backup of the retrieved data in case the script crashes (it's updated every iteration of the loop).  Therefore, if something happens you won't lose all your progress, and you can change k to equal where it was when the script crashed and run it again.  Both of these temporary files are deleted at the end of the script.
    
    At the end, it combines all the resulting data into {site_to_use}_export.JSON.  
    
  
## 3. json_error_checker.py

  VARIABLES TO DEFINE:
  - site_to_use --> Same as before
  - local_path --> Same as before
  - image_extension --> This is going to be the file extension of your uploaded images as a string, without the preceding period.  For us, we use JPEGs, so this value is "JPG".  You can find this value in the full file name of one of your images.
  - dropbox_token --> Same as before
  - classifier_url -- Same as before
  - coralnet_token --> Same as before
  
  This script takes the export JSON from coralnet_api_deployer.py and checks for errors, which occassionally occur.  The way coralnet_api_deployer.py is written, it can return errors for some images instead of data.  This checks for errors, and if some are detected, it attempts to fix them by sending new requests for just those images and overwrites the error data.  If none are detected, it will print "No errors!" and you are free to move onto json_parser.py.  If it detects errors but manages to fix them, it will run for a while but eventually print "A-OK!".  Otherwise it will print "STILL HAVE ISSUES!!!!", which means you can try running it again or you may need to look into potential issues in your internet/code (I personally have yet to have this script not fix errors on the first try).  This does not generate a new file (it overwrites {site_to_use}_export.JSON).
  
## 4. json_parser.py

  VARIABLES TO DEFINE:
  - site_to_use --> Same as before
  - local_path --> Same as before
  - image_extension --> This is going to be the file extension of your uploaded images as a string, without the preceding period. For us, we use JPEGs, so this value is "JPG". You can find this value in the full file name of one of your images.
  
  This script takes the export JSON file generated using coralnet_api_deployer.py and parses the data fields to store them in a dataframe.  This dataframe is in a similar (although not identical) format as the exported annotations files from the web version of CoralNet.  This is then exported as a .csv, and the filename is {site_to_use}.csv.
