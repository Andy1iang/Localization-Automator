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
    
    #Logs Language Saved
    print(f'{language} saved')
    
    
def save_language(language):
    if os.path.isfile(f'{script_path}/Spira-{language}.zip'):
        os.mkdir(f'{script_path}/Spira-{language}')
        shutil.move(f'Spira-{language}.zip',f'{script_path}/Spira-{language}')
        shutil.unpack_archive(f'{script_path}/Spira-{language}/Spira-{language}.zip',f'{script_path}/Spira-{language}')
            
    else: 
        print(f'Language file not found, Spira-{language}.zip missing')
            
    for file in os.listdir(f'{script_path}/Spira-{language}'):
        if re.match(r"\w+\." + language + "\.resx", file):
            for directory in ds.directories.items():
                if directory[0] in file:
                    new_name = file.replace(f'{directory[0]}_','')
                    os.rename(f'{script_path}/Spira-{language}/{file}',f'{script_path}/Spira-{language}/{new_name}')
                    if os.path.isfile(f'{dir_path}/{directory[1]}/{new_name}'):
                        print(f'Overwritten {new_name} in {dir_path}/{directory[1]}')
                        os.remove(f'{dir_path}/{directory[1]}/{new_name}')
                    shutil.move(f'{script_path}/Spira-{language}/{new_name}',f'{dir_path}/{directory[1]}')

    shutil.rmtree(f'{script_path}/Spira-{language}')
            


if __name__ == '__main__':

    possible_languages = ['cs', 'de', 'es', 'fi', 'fr', 'hu', 'pl', 'pt-pt', 'pt', 'ru', 'zh-Hans', 'zh-Hant']
    user_language = 'lorem'
    #checking if user's choice of languages are valid
    while user_language not in possible_languages and not set(user_language).issubset(set(possible_languages)) and not '':
        user_language = input(f'Press Enter to Bundle Default Languages:{ds.language}, or manually enter *separate using commas  \nLanguage: {possible_languages}\n')

        #If User does not enter anything, default language selections are saved
        if user_language == '':
            user_language = ds.language
            break
        
        #splitting up user input into a list and removing commas
        elif ',' in user_language:
            while ' ' in user_language:
                user_language = user_language.replace(' ','')
            user_language = user_language.split(',')

    #Checking if multiple languages need to be bundled
    if type(user_language) == list or type(user_language) == tuple:
        for language in user_language:
            export_language(language)
    
    else: 
        export_language(user_language)
        
    
   
    save_language(user_language)