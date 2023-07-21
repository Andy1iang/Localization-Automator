# Localization-Automator
bundler-for-translation is a python script with 3 functionalities
1. Export all resx files of a certain language
2. Import language files of a langauge (from zip file)
3. Updating language (resx) files and adding missing data

Before running this script, make sure it is located in the SpiraTeam/Design/Localization directory
If the importing feature will be used, make sure the zip files are also located in the SpiraTeam/Design/Localization directory
If the update feature will be used, make sure beautifulsoup4 is installed (pip install beautifulsoup4) 

To run the script: 
1. cd to the Localization directory in terminal
2. type this in the command line: python bundler-for-automation.py
   this will ask the user to input their choice to either export or import
   then it will ask the user if they want to use the default languages or choose their own manually

3. There are also other options to automate this process
   To automatically export the default languages: python bundler-for-automation.py --export
   To automatically import the default languages: python bundler-for-automation.py --import
   To automatically update the default langauges(for update): python bundler-for-automation.py --update

Outputs:
*All exported files will be in the same Directory as the script (SpiraTeam/Design/Localization)
*All updated resx files will overwrite previous ones in their original locations
*All temporary files will be deleted automatically

Configurations:
To edit default configurations, edit the variable fields in default_configs class
self.languages_update: tuple(immutable array) determines the default languages to be updated
self.language: tuple(immutable array) determines the default languages to be imported and/or exported
self.all_languages: tuple(immutable array) determines all languages that are supported
self.dictionaries: dictionary(key-value pairs) determines the prefix of resx files and its file path




