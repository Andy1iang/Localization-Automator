#importing Regex (Part of Standard Libraries)
import re

#importing Shell Utilities & OS Module (Part of Standard Libraries)
import shutil
import os

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

    parent_folders = []
    for folder in os.listdir(file_path):
        parent_folders.append(folder)

    for parent in parent_folders:
        if os.path.isdir(f'{file_path}/{parent}'):
            for folder in os.listdir(f'{file_path}/{parent}'):
                if os.path.isdir(f'{file_path}/{parent}/{folder}'):
                    for resx in os.listdir(f'{file_path}/{parent}/{folder}'):
                        if re.match(r"^[^.]*.resx[^.]*$", resx) or re.match(r"\w+\." + language + "\.resx", resx):
                            shutil.copyfile(f'{file_path}/{parent}/{folder}/{resx}', f'{parent}_{resx}')
                            shutil.move(f'{parent}_{resx}',f'{file_path}/Design/Localization/Spira-{language}')

    #Zips the temporary folder (moves if not in right folder) and deletes the temporary folder
    shutil.make_archive(f'Spira-{language}', format='zip', root_dir=file_path+'/Design/Localization/Spira-'+language)
    shutil.move(f'Spira-{language}.zip',f'{file_path}/Design/Localization')
    shutil.rmtree(f'{file_path}/Design/Localization/Spira-{language}')
    print(f'{language} saved')


if __name__ == '__main__':

    #Validates user's input for their file path
    user_file_path = 'lorem'
    while not os.path.exists(user_file_path):
        user_file_path = input('Please enter your file path, including SpiraTeam \nExample: /Users/andy/Desktop/Inflectra/SpiraTeam\n')

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