# Localization-Automator
bundler-for-translation is a python script with 3 functionalities
1. Export all resx files of a certain language
2. Import language files of a langauge (from zip file)
3. Updating language (resx) files and adding missing data (export & import functionalities)

<b>*Before running this script, make sure it is located in the SpiraTeam/Design/Localization directory<br>
*If the importing feature will be used, make sure the zip files are also located in the SpiraTeam/Design/Localization directory<br>
*If the update feature will be used, make sure beautifulsoup4 is installed (pip install beautifulsoup4) </b><br>
<br>
To run the script: 
1. cd to the Localization directory in terminal
2. type this in the command line: python bundler-for-automation.py
   this will ask the user to input their choice to either export or import
   then it will ask the user if they want to use the default languages or choose their own manually
   
3. There are also other options to automate this process
<ul>To automatically export the default languages: python bundler-for-automation.py --export</ul>
<ul>To automatically import the default languages: python bundler-for-automation.py --import</ul>
<ul>To automatically update the default langauges: 
   <br>----- To update files and export to 'QQQ' Folder: python bundler-for-automation.py --update --export
   <br>----- To import files from 'QQQ' Folder after changes: lpython bundler-for-automation.py --update --import
</ul>
<br>
Outputs:
<br><br>
<ul>All exported files will be in the same Directory as the script (SpiraTeam/Design/Localization)</ul>
<ul>All updated resx files will be saved in the same directory as the script (named 'QQQ-Spira-<i>language</i>')</ul>
<ul>All temporary files will be deleted automatically</ul>

<br>
Configurations:<br><br>
To edit default configurations, edit the variable fields in default_configs class<br><br>
<ul>self.languages_update: tuple(immutable array) determines the default languages to be updated</ul>
<ul>self.language: tuple(immutable array) determines the default languages to be imported and/or exported</ul>
<ul>self.all_languages: tuple(immutable array) determines all languages that are supported</ul>
<ul>self.dictionaries: dictionary(key-value pairs) determines the prefix of resx files and its file path</ul>
