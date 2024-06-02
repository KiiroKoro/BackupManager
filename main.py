'''
Configure all the settings for the backup such as
the destination, all the folders that should get backed up
and the time at which the automatic backup should take place
'''

from customtkinter import *
from tkinter import filedialog, Listbox
from os.path import exists
from datetime import date
import backup_libraries
import win32gui, win32con

the_program_to_hide = win32gui.GetForegroundWindow()
win32gui.ShowWindow(the_program_to_hide , win32con.SW_HIDE)


def main():
    folders_to_save = []
    dest: str = 'No folder currently selected'
    save_path: str = backup_libraries.save_path
    dest_label: CTkLabel = None
    next_save = date.today()
    language = 'english'
    time = ''

    button_texts = {
        'add': {'german': 'Ordner hinzufügen', 'english': 'Add folder'},
        'remove': {'german': 'Ordner verwerfen', 'english': 'Remove folder'},
        'destination': {'german': 'Zielordner auswählen', 'english': 'Select destination'},
        'backup': {'german': 'Manuelles backup', 'english': 'Manual backup'},
        'time': {'german': 'Automatisches Backup um:', 'english': 'Automatic backup at:'},
        'save': {'german': 'Einstellungen speichern', 'english': 'Save settings'}
    }


    def change_destination(frame: CTkFrame):
        dest = filedialog.askdirectory()
        dest_label = CTkLabel(master=frame,text=dest)
        dest_label.grid(row=1,column=2, padx=10,pady=10)
        backup_libraries.save(folders_to_save, dest, backup_time.get())

    def add_folder_to_backup(box: Listbox):
        selected_folder = filedialog.askdirectory()
        if len(selected_folder) <=1 or selected_folder in folders_to_save:
            return
        folders_to_save.append(selected_folder)
        box.insert(0,selected_folder)
        backup_libraries.save(folders_to_save, dest, backup_time.get())

    def remove_folder_to_backup(box: Listbox):
        selected_folder_index = box.curselection()
        selected_folder = box.get(selected_folder_index)
        folders_to_save.remove(selected_folder)
        box.delete(selected_folder_index)
        backup_libraries.save(folders_to_save, dest, backup_time.get())

    # Function decleration done, now the UI
    if exists(save_path):
        dest, time, folders_to_save = backup_libraries.load()

    root = CTk()
    root.geometry("500x550")
    root.title("Backup manager")
    
    box = Listbox(master=root)
    for folder in folders_to_save:
        box.insert(0,folder)
    box.config(width=60,height=10)
    box.pack(padx=10,pady=10)

    frame = CTkFrame(master=root)
    frame.pack(padx=10,pady=5)   

    add_btn = CTkButton(master=frame,text=button_texts['add'][language.lower()],command=lambda: add_folder_to_backup(box))
    add_btn.grid(row=1,column=1, padx=10,pady=10)

    remove_btn = CTkButton(master=frame,text=button_texts['remove'][language.lower()],command=lambda: remove_folder_to_backup(box))
    remove_btn.grid(row=2,column=1, padx=10,pady=10)

    frame2 = CTkFrame(master=root)
    frame2.pack(padx=10,pady=10)

    dest_btn = CTkButton(master=frame2,text=button_texts['destination'][language.lower()],command=lambda: change_destination(frame2))
    dest_btn.grid(row=1,column=1, padx=10,pady=10)
    dest_label = CTkLabel(master=frame2,text=dest)
    dest_label.grid(row=1,column=2, padx=10,pady=10)

    frame3 = CTkFrame(master=root)
    frame3.pack(padx=10,pady=10)

    manual_backup = CTkButton(master=frame3,text=button_texts['backup'][language.lower()],command=lambda: backup_libraries.backup(True))
    manual_backup.grid(row=1,column=1, padx=10,pady=10)

    backup_time = CTkEntry(master=root,placeholder_text=button_texts['time'][language.lower()],width=180)
    if time:
        time = time[:2]+':'+time[2:]
    backup_time.insert(0,time)
    backup_time.pack(padx=10,pady=10)
    backup_time_save = CTkButton(master=root,text=button_texts['save'][language.lower()],command=lambda: backup_libraries.save(folders_to_save,dest,backup_time.get()))
    backup_time_save.pack(padx=10,pady=10)

    root.mainloop()

if __name__ == '__main__':
    main()