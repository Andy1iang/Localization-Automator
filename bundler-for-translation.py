'''
This Python Script should be in the directory of SpiraTeam/Design/Localization
'''
#importing Regex (Part of Standard Libraries) to check file names
import re

#importing Shell Utilities & OS Module (Part of Standard Libraries) to move
import shutil
import os

#importing sys (Part of Standard Libraries) to take in command line calls
import sys

#importing bs4 (Not Part of Standard Libraries) to read & write resx files
from bs4 import BeautifulSoup   #To Install on command line:  pip install beautifulsoup4

#Script is located in SpiraTeam/Design/Localization
#Goes up 2 directories to access the SpiraTeam directory
script_path = os.getcwd()
sub_path = os.path.abspath(os.path.join(script_path, os.pardir))
dir_path = os.path.abspath(os.path.join(sub_path, os.pardir)) #SpiraTeam Directory

#Default Configuration Class
class default_config:
    def __init__(self): 
        self.languagesUpdate = ('es', 'pt') #Edit to change languages to update
        self.language = ('fr', 'de') #Edit to Change Default Languages
        self.all_languages = ['cs', 'de', 'es', 'fi', 'fr', 'hu', 'pl', 'pt-pt', 'pt', 'ru', 'zh-Hans', 'zh-Hant'] #Edit to Change Supported Languages
        self.directories = { # Edit to Change Default Directories that Store resx Files
            'business': '/Business/GlobalResources',
            'web':'/SpiraTest/App_GlobalResources',
            'common':'/Common/Resources',
        }

#Default instance
ds = default_config()

#Function to copy files from source location to Destination
def copy_files(language, sub_file_path, file_type, file_name):
    '''
    language: language selected by the user
    sub_file_path: File path from SpiraTeam to resx file folders
    type: Folder the resx file is in
    file_name: name of the file in original location
    '''
    if re.match(r"^[^.]*.resx[^.]*$", file_name) or re.match(r"\w+\." + language + "\.resx", file_name):
        shutil.copyfile(f'{dir_path}{sub_file_path}/{file_name}', f'{file_type}_{file_name}')
        shutil.move(f'{file_type}_{file_name}',f'{dir_path}/Design/Localization/Spira-{language}')
        
#Function Create New Zip File with English and Chosen Language resx Files
def export_language(language):
    '''
    language: language selected by the user
    '''
    #Checking a File with name of Spira-'language' exists, deletes if it is
    if os.path.exists(f'{dir_path}/Design/Localization/Spira-{language}'):
        print('File Exists, Overwriting File')
        shutil.rmtree(f'{dir_path}/Design/Localization/Spira-{language}')

    #Creates new temporary folder to hold resx files
    os.mkdir(f'{dir_path}/Design/Localization/Spira-{language}')
    
    #Loops through all key-value pairs for default file paths
    for prefix, directory in ds.directories.items():
        for files in os.listdir(f'{dir_path}/{directory}'):
            #saves files to to a temporary folder in Design/Localization
            copy_files(language,directory,prefix,files)

    #Zips the temporary folder (moves if not in right folder) and deletes the temporary folder
    if os.path.isfile(f'{dir_path}/Design/Localization/Spira-{language}.zip'):
        os.remove(f'{dir_path}/Design/Localization/Spira-{language}.zip')
    shutil.make_archive(f'Spira-{language}', format='zip', root_dir=dir_path+'/Design/Localization/Spira-'+language)
    
    #Deletes Temporary File
    shutil.rmtree(f'{dir_path}/Design/Localization/Spira-{language}')
    
    #Logs Language Exported
    print(f'{language} Exported')
    
#Function to import and overwrite current resx files with new ones from zip files
def import_language(language):
    '''
    language: language selected by the user
    language zip files should be in the same directory as the python script (Design/Localization)
    '''
    #Checking if the language file is in the same directory as the 
    if os.path.isfile(f'{script_path}/Spira-{language}.zip'):
        #making folder to store zip file & moving zip file & unzipping the file
        os.mkdir(f'{script_path}/Spira-{language}')
        shutil.move(f'Spira-{language}.zip',f'{script_path}/Spira-{language}')
        shutil.unpack_archive(f'{script_path}/Spira-{language}/Spira-{language}.zip',f'{script_path}/Spira-{language}')
        
        #looping through all files of a language folder (unzipped)
        for file in os.listdir(f'{script_path}/Spira-{language}'):
            #matching name using regex
            if re.match(r"\w+\." + language + "\.resx", file):
                
                #Loops through all key-value pairs for default file paths
                for prefix, directory in ds.directories.items():
                    #checking if prefix matches the file name
                    if prefix in file:
                        #renaming the file (getting rid of prefix)
                        new_name = file.replace(f'{prefix}_','')
                        os.rename(f'{script_path}/Spira-{language}/{file}',f'{script_path}/Spira-{language}/{new_name}')
                        #overwriting the original file
                        if os.path.isfile(f'{dir_path}/{directory}/{new_name}'):
                            os.remove(f'{dir_path}/{directory}/{new_name}')
                        shutil.move(f'{script_path}/Spira-{language}/{new_name}',f'{dir_path}/{directory}')

        #deleting unzipped folder
        shutil.rmtree(f'{script_path}/Spira-{language}')
        print(f'{language} Imported')
            
    else: 
        #if zip file is not found, this prints
        print(f'Language file not found, Spira-{language}.zip missing')
            
#function that allows the using to choose a language
def choose_language():
    user_language = 'lorem'
    #checking if user's choice of languages are valid
    while user_language not in ds.all_languages and not set(user_language).issubset(set(ds.all_languages)) and not '':
        user_language = input(f'Press Enter to Choose Default Languages:{ds.language}, or manually enter *separate using commas  \nLanguage: {ds.all_languages}\n')

        #If User does not enter anything, default language selections are saved
        if user_language == '':
            user_language = ds.language
        
        #splitting up user input into a list and removing commas
        elif ',' in user_language:
            while ' ' in user_language:
                user_language = user_language.replace(' ','')
            user_language = user_language.split(',')
        
    return user_language


if __name__ == '__main__':
    
    '''
    Command line calls:
    To prompt user inputs:    python bundler-for-automation.py 
    To automatically export default languages:    python bundler-for-automation.py --export 
    To automatically import default languages:    python bundler-for-automation.py --import 
    '''
    if len(sys.argv) == 2: #checking if additional argument is passed in command line call
        
        #exports all default languages
        if sys.argv[1].lower() == '--export':
            for language in ds.language:
                export_language(language)
        
        #imports all default languages
        elif sys.argv[1].lower() == '--import':
            for language in ds.language:
                import_language(language)
                
        #updates current languages
        elif sys.argv[1].lower() == '--update':
            with open('Buttons1.es.resx','r') as f:
                data = f.read()
            Bs_data = BeautifulSoup(data, "xml")
            Bs_data = list(Bs_data.findAll('data'))
            my_data = []
            for element in Bs_data:
                my_data.append(str(element))
            print(my_data[144])
            print(re.search(r'name="\w+"',my_data[144]).string)
            print(my_data[144][6:25])
                
        #prints this is argument is invalid      
        else:
            print('Argument not valid')
        
    else:
        #using chooses whether to import or to export
        user_choice = 'wrong'
        while user_choice != 'import' and user_choice != 'export':
            user_choice = input('Import or Export Files? Enter "import" or "export"\n').lower()
            
        user_language = choose_language()
        
        if user_choice == 'export':
            #Checking if multiple languages need to be bundled
            if type(user_language) == list or type(user_language) == tuple:
                for language in user_language:
                    export_language(language)
        
            else: 
                export_language(user_language)
            
            
        if user_choice == 'import':
            #Checking if multiple languages need to be imported
            if type(user_language) == list or type(user_language) == tuple:
                for language in user_language:
                    import_language(language)
        
            else: 
                import_language(user_language)