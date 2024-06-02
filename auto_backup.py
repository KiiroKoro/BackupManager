'''
Put this in the startup-folder in order to automatically save a backup
at the given time
'''

import backup_libraries
from datetime import datetime
from time import sleep
import win32gui, win32con

the_program_to_hide = win32gui.GetForegroundWindow()
win32gui.ShowWindow(the_program_to_hide , win32con.SW_HIDE)

def main():
    save_time = ''
    with open(backup_libraries.save_path) as f:
        content = f.read()
        save_time = content.split('\n')[1]

    if backup_libraries.already_backed_up():
        return

    check = True
    while(check):
        current_time = datetime.now().time()
        current_hour = current_time.hour
        current_minute = current_time.minute

        if current_hour > int(save_time[:2]):
            try:
                backup_libraries.backup()
            except Exception as e:
                input(e)
            check = False
        
        elif current_hour == int(save_time[:2]):
            if current_minute >= int(save_time[2:]):
                try:
                    backup_libraries.backup()
                except Exception as e:
                    input(e)
                check = False
        
        if check:
            sleep(30)


if __name__ == '__main__':
    main()