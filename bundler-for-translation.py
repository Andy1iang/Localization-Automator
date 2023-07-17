'''
This Python Script should be in the directory of SpiraTeam/Design/Localization
'''
#importing Regex (Part of Standard Libraries)
import re

#importing Shell Utilities & OS Module (Part of Standard Libraries)
import shutil
import os

#Script is located in SpiraTeam/Design/Localization
#Goes up 2 directories to access the SpiraTeam directory
script_path = os.getcwd()
sub_path = os.path.abspath(os.path.join(script_path, os.pardir))
dir_path = os.path.abspath(os.path.join(sub_path, os.pardir)) #SpiraTeam Directory

#Default Configuration Class
class default_config:
    def __init__(self): 
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
    for directory in ds.directories.items():
        for files in os.listdir(f'{dir_path}/{directory[1]}'):
            #saves files to to a temporary folder in Design/Localization
            copy_files(language,directory[1],directory[0],files)

    #Zips the temporary folder (moves if not in right folder) and deletes the temporary folder
    if os.path.isfile(f'{dir_path}/Design/Localization/Spira-{language}.zip'):
        os.remove(f'{dir_path}/Design/Localization/Spira-{language}.zip')
    shutil.make_archive(f'Spira-{language}', format='zip', root_dir=dir_path+'/Design/Localization/Spira-'+language)
    
    #Deletes Temporary File
    shutil.rmtree(f'{dir_path}/Design/Localization/Spira-{language}')
    
    #Logs Language Exported
    print(f'{language} Exported')
    
#Function to save and overwrite current resx files with new ones from zip files
def save_language(language):
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
                
                for prefix, directory in ds.directories.items():
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
        print(f'{language} Saved')
            
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
    
    #using chooses whether to save or to export
    user_choice = 'wrong'
    while user_choice != 'save' and user_choice != 'export':
        user_choice = input('Save or Export Files? Enter "save" or "export"\n').lower()
        
    user_language = choose_language()
    
    if user_choice == 'export':
        #Checking if multiple languages need to be bundled
        if type(user_language) == list or type(user_language) == tuple:
            for language in user_language:
                export_language(language)
    
        else: 
            export_language(user_language)
        
        
    if user_choice == 'save':
        #Checking if multiple languages need to be saved
        if type(user_language) == list or type(user_language) == tuple:
            for language in user_language:
                save_language(language)
    
        else: 
            save_language(user_language)