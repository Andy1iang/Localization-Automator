'''
This Python Script should be in the directory of SpiraTeam/Design/Localization
Need to install beautifulsoup4 before running: pip install beautifulsoup4
'''
#importing Regex (Part of Standard Libraries) to check file names
import re

#importing Shell Utilities & OS Module (Part of Standard Libraries) to move
import shutil
import os

#importing sys (Part of Standard Libraries) to take in command line calls
import sys

#importing bs4 (Not Part of Standard Libraries) to read resx files
from bs4 import BeautifulSoup   #To Install on command line:  pip install beautifulsoup4

#importing ElementTree to write to resx files
import xml.etree.ElementTree as ET

#Script is located in SpiraTeam/Design/Localization
#Goes up 2 directories to access the SpiraTeam directory
script_path = os.getcwd()
sub_path = os.path.abspath(os.path.join(script_path, os.pardir))
dir_path = os.path.abspath(os.path.join(sub_path, os.pardir)) #SpiraTeam Directory

#Default Configuration Class
class default_config:
    def __init__(self): 
        self.languages_update = ('es', 'pt') #Edit to change languages to update
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
        for file in os.listdir(f'{script_path}/Spira-{language}/Spira-{language}'):
            
            #matching name using regex
            if re.match(r"\w+\." + language + "\.resx", file):
                
                #Loops through all key-value pairs for default file paths
                for prefix, directory in ds.directories.items():
                    #checking if prefix matches the file name
                    if prefix in file:
                        #renaming the file (getting rid of prefix)
                        new_name = file.replace(f'{prefix}_','')
                        os.rename(f'{script_path}/Spira-{language}/Spira-{language}/{file}',f'{script_path}/Spira-{language}/Spira-{language}/{new_name}')
                        #overwriting the original file
                        if os.path.isfile(f'{dir_path}/{directory}/{new_name}'):
                            os.remove(f'{dir_path}/{directory}/{new_name}')
                        shutil.move(f'{script_path}/Spira-{language}/Spira-{language}/{new_name}',f'{dir_path}{directory}/{new_name}')
                        

        #deleting unzipped folder
        shutil.rmtree(f'{script_path}/Spira-{language}')
        print(f'{language} Imported')
            
    else: 
        #if zip file is not found, this prints
        print(f'Language file not found, Spira-{language}.zip missing')

#helper function to copy primary and language files to script directory
def bundle_language(language):
    '''
    language: language selected by the user
    '''
    #Checking a File with name of Spira-'language' exists, deletes if it is
    if os.path.exists(f'{dir_path}/Design/Localization/Spira-{language}'):
        shutil.rmtree(f'{dir_path}/Design/Localization/Spira-{language}')

    #Creates new temporary folder to hold resx files
    os.mkdir(f'{dir_path}/Design/Localization/Spira-{language}')
    
    #Loops through all key-value pairs for default file paths
    for prefix, directory in ds.directories.items():
        for files in os.listdir(f'{dir_path}/{directory}'):
            #saves files to to a temporary folder in Design/Localization
            copy_files(language,directory,prefix,files)
            
    
            
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

#helper function to update missing data to language files
def make_dictionary(language,file_name):
    '''
    language: user's choice of language
    file_name: file name to be read from (resx)
    '''
    with open(f'{script_path}/Spira-{language}/{file_name}','r',encoding= 'utf-8') as f:
        data = f.read() #reading the file
        
        #making beautifulsoup data into a list
        bs_data = BeautifulSoup(data, "xml")
        list_data = list(bs_data.findAll('data'))
        
        #creating key value pairs for each data element 
        data_dict = {}
        for element in list_data:
            element  = str(element)
            if re.search(r'name="\w+"',element):
                name = re.search(r'name="\w+"',element).span()   
            data_dict[element[name[0]+6:name[1]-1]] = element
            
    return data_dict

#helper function to save the updated resx files back to original location
def save_update(language):
    '''
    language: user's choice of language
    '''
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
                    shutil.move(f'{script_path}/Spira-{language}/{new_name}',f'{dir_path}{directory}')

    #deleting temp folder
    shutil.rmtree(f'{script_path}/Spira-{language}')


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
                
        #updates missing data to language files
        elif sys.argv[1].lower() == '--update':
            
            for language in ds.languages_update:
                
                bundle_language(language) #getting language files 
                
                for file_name in os.listdir(f'{script_path}/Spira-{language}'):
                    #matching all files that are primary (english) files
                    if re.match(r"^[^.]*.resx[^.]*$", file_name):
                        
                        #parsing through file to write to it later
                        eng_tree = ET.parse(f'{script_path}/Spira-{language}/{file_name}')
                        eng_root = eng_tree.getroot()
                        lang_file_name = file_name.replace('.',f'.{language}.')
                        lang_tree = ET.parse(f'{script_path}/Spira-{language}/{lang_file_name}')
                        lang_root = lang_tree.getroot()
                        
                        #making key value pairs of primary and language files
                        eng_dict = make_dictionary(language,file_name)
                        lang_dict = make_dictionary(language,lang_file_name)

                        #checking if the data name exists in language file
                        for key,value in eng_dict.items():
                            try:
                                lang_dict[key]
                            except:
                                lang_dict[key] = value
                                
                                #copying data from primary file to language file
                                add_string = str(eng_dict[key])
                                temp_value = re.search(r'<value>[\s\S]*</value>',add_string).span()
                                temp_string = add_string[temp_value[0]:temp_value[1]]
                                
                                #formatting the string
                                #subString from 7 to -8 is the value without "<value> tag"
                                add_string = add_string.replace(temp_string,f'    <value>QQQ {temp_string[7:-8]}</value>') #adding QQQ to mark missing
                                add_string = add_string.replace("</data>", "  </data>\n")
                                add_string = add_string.replace("<data", "  <data")
                                
                                #adding to language resx file
                                add_string = ET.fromstring(add_string)
                                lang_root.append(add_string)
                                
                        #writing to resx file
                        lang_tree.write(f'{script_path}/Spira-{language}/{lang_file_name}')
                
                #moving updated files back to original location (language only)    
                save_update(language)

                #logging finished process
                print(f'{language} Updated')
                    
                
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