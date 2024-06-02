'''
Library for functionality of the other two programs
'''

from os.path import exists
from os import remove, listdir, makedirs
from datetime import date
from shutil import copy

save_path: str = 'C:/Desktop/save.dirs'

def save(folders_to_save, dest: str, time: str):
    '''
    Saves the users backup settings
    '''
    if exists(save_path):
        remove(save_path)
    with open(save_path,'x') as f:
        f.write(dest + '\n')
        time = time.replace(':','')
        f.write(('0'*(4-len(time))) + time + '\n')
        for folder in folders_to_save:
            f.write(folder + '\n')
    print(f'Saved settings to {save_path}')


def load():
    '''
    Returns the folders that are supposed to get backed up
    as well as the destination in which the backup gets saved
    '''
    folders_to_save = []
    lines = []
    with open(save_path,'r') as file:
        content = file.read()
        lines = [line for line in content.split('\n')]
    dest = lines[0]
    time = lines[1]
    for folder in lines[2:]:
        if len(folder) > 1:
            folders_to_save.append(folder)
    
    return dest, time, folders_to_save


def backup(manual: bool = False):
    '''
    Takes all files out of the folders the user specified and
    copies them into the destination-folder
    '''
    dest, _, folders_to_save = load()

    # MOST IMPORTANT PART
    new_dest = f"{dest}/{str(date.today())}{' (manual)' if manual else ''}"
    i: int = 2
    if exists(new_dest):
        while exists(new_dest + f" ({i})"):
            i += 1
        new_dest += f" ({i})"
    makedirs(new_dest)

    for folder in folders_to_save:
        try:
            current_dest = f"{new_dest}/{folder[folder.rfind('/')+1:]}"
            makedirs(current_dest)
            for file in listdir(folder):
                copy(folder+'\\'+file,current_dest)
        except:
            pass
    if manual:
        print(f'Created a manual backup at {dest}')

def already_backed_up() -> bool:
    dest,_,_ = load()
    return exists(f"{dest}/{str(date.today())}")
    