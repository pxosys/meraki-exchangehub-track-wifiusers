# Setup + Installation
    1. Download repository and move to desired directory
    2. Run `pip install -r requirements.txt` to install any potentially missing packages
    3. Go to the Meraki Dashboard and generate an API key for yourself. If you need assistance on obtaining an API Key, please visit https://documentation.meraki.com/zGeneral_Administration/Other_Topics/The_Cisco_Meraki_Dashboard_API
    4. Paste this value into the provided credentials.json file (if desired)
    5. Run script. For instructions on running the script, read below

# Instructions
The script obtains its credentials in two ways: 
- Imported from a JSON file using the --credentials argument
- Specifically designated using the --apiKey argument

The --reportMode argument (which defaults to "client") can be used to change the output of the script to a dict of each device that is detected.

To run the script, enter `python[3] main.py [arguments]` and the script will begin, requiring no further input


# Description
The script will output a dict that can list either the devices that have connected to your devices or the devices themselves. Default output mode is the clients, which can be used for tracking an individual device as it moves around 

