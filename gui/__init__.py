from customtkinter import *
from tkinter import *
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from tkinter import font as font
import os, datetime, time, sys, threading, webbrowser
import random

class THEME:
    PRIMARY_COLOR = "#1F2429"
    PRIMARY_COLOR_LIGHT = "#2C313A"
    SECONDARY_COLOR = "#19C09F"
    SECONDARY_COLOR_LIGHT = "#63C3B0"
    TEXT_COLOR = "#FFFFFF"
    FONT = ("Helvetica", 12)
    
class GUI(CTk):
    app_sloganları = ["Bir klasör seçin", "Dosyalarınızı düzenleyin", "Verimliliğinizi artırın"]
    gecerli_app_sloganı = random.choice(app_sloganları)
    newStarted = True
    
    def __init__(self):
        super().__init__()
        self.title(f"File Organizer - {self.gecerli_app_sloganı}")
        self.minsize(1350,750)
        self.maxsize(1350,750)
        self.resizable(False, False)
        self.config(bg=THEME.PRIMARY_COLOR)
        
        self.create_widgets()
        
    def create_widgets(self):
        self.bottom_area = CTkFrame(self, bg_color=THEME.PRIMARY_COLOR, fg_color=THEME.PRIMARY_COLOR_LIGHT)
        self.bottom_area.pack(side=BOTTOM, fill=X, padx=10, pady=10)
        
        self.fileSelectorButton = CTkButton(self.bottom_area, 
                                            bg_color=THEME.PRIMARY_COLOR_LIGHT, 
                                            fg_color=THEME.SECONDARY_COLOR, 
                                            hover_color=THEME.SECONDARY_COLOR_LIGHT,
                                            text="Klasör Seç", 
                                            command=self.select_folder, 
                                            font=("Arial", 14),
                                            corner_radius=6.25,
                                            height=30
                                            )
        self.fileSelectorButton.pack(side=RIGHT, padx=(0,5), pady=5)
        
        self.fileDirectoryEntry = CTkEntry(self.bottom_area,
                                           height=30, 
                                           placeholder_text="Klasör yolu", 
                                           font=("Arial", 14),
                                           bg_color=THEME.PRIMARY_COLOR_LIGHT,
                                           fg_color=THEME.PRIMARY_COLOR_LIGHT,
                                           text_color=THEME.TEXT_COLOR,
                                           border_width=0,
                                           )
        self.fileDirectoryEntry.pack(side=LEFT, fill=X, expand=True, padx=5, pady=5)
        
        if self.newStarted:
            self.welcomeMessageFrame = CTkFrame(self, bg_color=THEME.PRIMARY_COLOR, fg_color=THEME.PRIMARY_COLOR_LIGHT)
            self.welcomeMessageFrame.pack(side=TOP, fill=BOTH)
            

    def select_folder(self):
        folder_path = fd.askdirectory()
        if folder_path:
            self.process_files(folder_path)

    def select_folder(self):
        folder_path = fd.askdirectory()
        if folder_path:
            self.process_files(folder_path)

    def process_files(self, folder_path):
        ...
        
def start():
    app = GUI()
    app.mainloop()
    
if __name__ == "__main__":
    start()