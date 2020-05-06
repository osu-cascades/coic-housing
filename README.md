# Readme

## What
This new code gets user input for census acs years, pulls the data,transforms with pandas, and saves to GSheets.
With Tableau public (not desktop!), you can have your data automatically sync (every 24 hours it updates but can be done manually if needed sooner).

## Who
Taylor Malory: taymal1987@gmail.com    
Matthew Barnes: mlbarnes04@gmail.com

## Getting Started
* Make sure you have python 3 (Heroku is currently running 3.8), Anaconda (>= 4.6) and Git.
* Clone and `cd` into the repo
* Create a new virtual enviroment with `conda create --name myenv && conda activate myenv`, substituting `myenv` with whatever enviroment name you choose.
* Install dependencies with `conda install --file requirements.txt`
* You are now ready to edit the files and push to Heroku, so long as you have access to the project.


## Tips
* Ensure you have proper enviroment variables configured. These are denoted with `os.environ['SOME_ENV_VAR']`, except for the pygsheets authorization which just needs the key name. 
* The enviroment variables should be good to go and not need changing or updating. If they do, for some reason, those can be updated in Heroku either through the CLI or site. The 'service account' enviroment variable is a JSON file, generated through the projects Google Developers page (https://console.developers.google.com/), and thrown directly into Heroku as an eviroment variable. If, for some reason, the project needs a new one, generate it through the above link, add the **entire** file as an enviroment variable, and then share access to the email address within the JSON file from the projects sheets page.

### Links: 
* Python: https://www.python.org/downloads/
* Pandas: https://pandas.pydata.org/
* pygsheets: https://pypi.org/project/gsheets/
* requests: https://requests.readthedocs.io/en/master/
