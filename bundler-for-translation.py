#importing Regex (Part of Standard Libraries)
import re

#importing Shell Utilities & OS Module (Part of Standard Libraries)
import shutil
import os

#Function to copy files from source location to Destination
def copy_files(language, file_path, sub_file_path, type, file_name):
    '''
    language: language selected by the user
    file_path: user's file path to SpiraTeam
    sub_file_path: File path from SpiraTeam to resx file folders
    type: Folder the resx file is in
    file_name: name of the file in original location
    '''
    if re.match(r"^[^.]*.resx[^.]*$", file_name) or re.match(r"\w+\." + language + "\.resx", file_name):
        shutil.copyfile(f'{file_path}{sub_file_path}/{file_name}', f'{type}_{file_name}')
        shutil.move(f'{type}_{file_name}',f'{file_path}/Design/Localization/Spira-{language}')

#Function Create New Zip File with English and Chosen Language resx Files
def bundle_language(language, file_path):
    '''
    language: language selected by the user
    file_path: user's file path to SpiraTeam
    '''
    #Checking a File with name of Spira-'language' exists, deletes if it is
    if os.path.exists(f'{file_path}/Design/Localization/Spira-{language}'):
        print('File Exists, Overwriting File')
        shutil.rmtree(f'{file_path}/Design/Localization/Spira-{language}')

    #Creates new temporary folder to hold resx files
    os.mkdir(f'{file_path}/Design/Localization/Spira-{language}')

    #Goes through three folders that hold resx files and calls copy_files function
    for files in os.listdir(f'{file_path}/Business/GlobalResources'):
        copy_files(language, file_path, '/Business/GlobalResources', 'business', files)

    for files in os.listdir(f'{file_path}/SpiraTest/App_GlobalResources'):
        copy_files(language, file_path, '/SpiraTest/App_GlobalResources', 'web', files)

    for files in os.listdir(f'{file_path}/Common/Resources'):
        copy_files(language, file_path, '/Common/Resources', 'common', files)

    #Zips the temporary folder and deletes the temporary folder
    shutil.make_archive(f'Spira-{language}', format='zip', root_dir=file_path+'/Design/Localization/Spira-'+language)
    shutil.rmtree(f'{file_path}/Design/Localization/Spira-{language}')
    print(f'{language} saved')


if __name__ == '__main__':

    #Validates user's input for their file path
    user_file_path = 'lorem'
    while not os.path.exists(user_file_path):
        user_file_path = input('Please enter your file path, including SpiraTeam \nExample: /Users/andy/Desktop/Inflectra/Translation-Automator/SpiraTeam\n')

    #validates the user chose a valid language
    possible_languages = ['cs', 'de', 'es', 'fi', 'fr', 'hu', 'pl', 'pt-pt', 'pt', 'ru', 'zh-Hans', 'zh-Hant']
    user_language = 'lorem'
    #checking if user's choice of languages are valid
    while user_language not in possible_languages and not set(user_language).issubset(set(possible_languages)):
        user_language = input(f'Please choose a language(s) to bundle, separate using commas  \nLanguage: {possible_languages}\n')
        #splitting up user input into a list and removing commas
        if ',' in user_language:
            while ' ' in user_language:
                user_language = user_language.replace(' ','')
            user_language = user_language.split(',')

    #Checking if multiple languages need to be bundled
    if type(user_language) == list:
        for language in user_language:
            bundle_language(language, user_file_path)
    
    else: 
        bundle_language(user_language, user_file_path)