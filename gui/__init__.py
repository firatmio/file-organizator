from customtkinter import *
from tkinter import *
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from tkinter import font as font
import os, datetime, time, sys, threading, webbrowser, random, subprocess
from PIL import Image, ImageTk
from utils.organizer import organization

class THEME:
    PRIMARY_COLOR = "#202020"
    PRIMARY_COLOR_LIGHT = "#303030"
    PRIMARY_COLOR_EXTRA_LIGHT = "#404040"
    SECONDARY_COLOR = "#FFFFFF"
    SECONDARY_COLOR_LIGHT = "#D8D8D8"
    TEXT_COLOR_RESERVE = ("#000000", "#202020")
    TEXT_COLOR = "#FFFFFF"
    FONT = ("Helvetica", 12)
    
class GUI(CTk):
    app_sloganları = ["Bir klasör seçin", "Dosyalarınızı düzenleyin", "Verimliliğinizi artırın"]
    gecerli_app_sloganı = random.choice(app_sloganları)
    newStarted = True
    selectedFolder = None
    
    def __init__(self):
        super().__init__()
        self.title(f"File Organizator - {self.gecerli_app_sloganı}")
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
                                            text_color=THEME.TEXT_COLOR_RESERVE[1],
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
        self.fileDirectoryEntry.delete(0, END)
        self.fileDirectoryEntry.insert(0, "Bir klasör seç.")
        self.fileDirectoryEntry.configure(state=DISABLED)
        
        self.appContent()
        
    def appContent(self):
        try:
            self.appcontent.destroy()
            self.welcomeMessageFrame.destroy()
            self.content.destroy()
        except:
            pass
        
        self.appcontent = CTkFrame(self, bg_color=THEME.PRIMARY_COLOR, fg_color=THEME.PRIMARY_COLOR)
        self.appcontent.pack(fill=BOTH, expand=True)
        
        if self.newStarted:
            self.welcomeMessageFrame = CTkFrame(self.appcontent, bg_color=THEME.PRIMARY_COLOR, fg_color=THEME.PRIMARY_COLOR)
            self.welcomeMessageFrame.pack(expand=True, fill=BOTH, padx=20, pady=20)
            
            self.welcomePageHeader = CTkLabel(self.welcomeMessageFrame, text="File Organizator", font=("Arial", 72, "bold"), text_color=THEME.PRIMARY_COLOR_EXTRA_LIGHT)
            self.welcomePageHeader.pack(side=TOP, pady=(144, 0))
            
            self.welcomePageText = CTkLabel(self.welcomeMessageFrame,
                                            text="Bir dosya seçin, organize edin ve verimliliğinizi artırın.",
                                            text_color=THEME.PRIMARY_COLOR_LIGHT,
                                            bg_color=THEME.PRIMARY_COLOR,
                                            fg_color=THEME.PRIMARY_COLOR,
                                            font=("Arial", 24))
            self.welcomePageText.pack(side=TOP, pady=(20, 0))
            
        else:            
            self.appcontent.destroy()
            
            self.content = CTkFrame(self, bg_color=THEME.PRIMARY_COLOR, fg_color=THEME.PRIMARY_COLOR)
            self.content.pack(fill=BOTH, expand=False, padx=0, pady=0)
            
            self.infoArea = CTkFrame(self.content, bg_color=THEME.PRIMARY_COLOR, fg_color=THEME.PRIMARY_COLOR)
            self.infoArea.pack(side=TOP, fill=X, padx=0, pady=0)
            
            folder_img_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "folder.png")
            try:
                folder_img = Image.open(folder_img_path)
                try:
                    resample_filter = Image.Resampling.LANCZOS
                except AttributeError:
                    resample_filter = getattr(Image, "LANCZOS", Image.BICUBIC)

                folder_img = folder_img.resize((128, 128), resample=resample_filter)
                self.folder_icon = ImageTk.PhotoImage(folder_img)
                self.folderIconLabel = CTkLabel(self.infoArea, image=self.folder_icon, text="", bg_color=THEME.PRIMARY_COLOR, fg_color=THEME.PRIMARY_COLOR_LIGHT, corner_radius=10, width=200, height=200, cursor="hand2")
                self.folderIconLabel.pack(side=LEFT, pady=(50, 20), padx=(60, 0))
                self.folderIconLabel.bind("<Button-1>", lambda e: self.open_selected_folder())
                self.folderIconLabel.bind("<Enter>", lambda e: self.folderIconLabel.configure(fg_color=THEME.PRIMARY_COLOR_EXTRA_LIGHT))
                self.folderIconLabel.bind("<Leave>", lambda e: self.folderIconLabel.configure(fg_color=THEME.PRIMARY_COLOR_LIGHT))
            except Exception as e:
                self.folderIconLabel = CTkLabel(self.infoArea, text="Folder\nIcon", font=("Arial", 24), text_color=THEME.PRIMARY_COLOR_EXTRA_LIGHT, bg_color=THEME.PRIMARY_COLOR, fg_color=THEME.PRIMARY_COLOR_LIGHT, corner_radius=10, width=200, height=200)
                self.folderIconLabel.pack(side=LEFT, pady=(50, 20), padx=(60, 0))
            
            self.folderNameText = os.path.basename(self.selectedFolder) if self.selectedFolder else "Unknown"
            
            self.folderName = CTkLabel(self.infoArea, bg_color=THEME.PRIMARY_COLOR, fg_color=THEME.PRIMARY_COLOR, text_color=THEME.TEXT_COLOR, font=("Arial", 84), text=self.folderNameText)
            self.folderName.place(x=300, y=50)
            
            self.isSpecialFolder = BooleanVar(value=True)

            self.special_folder_checkbox = CTkCheckBox(
                self.infoArea,
                text="Bilinmeyen dosya türleri için 'Özel' klasörü oluşturulsun.",
                variable=self.isSpecialFolder,
                font=("Arial", 14),
                text_color=THEME.TEXT_COLOR,
                bg_color=THEME.PRIMARY_COLOR,
                fg_color=THEME.PRIMARY_COLOR_LIGHT,
                hover_color=THEME.PRIMARY_COLOR_EXTRA_LIGHT,
            )
            self.special_folder_checkbox.place(x=300, y=160)

            self.start_edit_button = CTkButton(
                self.infoArea,
                command=self.start_org,
                text="Organize Et",
                font=("Arial", 18),
                text_color=THEME.TEXT_COLOR_RESERVE[1],
                corner_radius=10,
                bg_color=THEME.PRIMARY_COLOR,
                fg_color=THEME.SECONDARY_COLOR,
                hover_color=THEME.SECONDARY_COLOR_LIGHT,
                height=36
            )
            self.start_edit_button.place(x=300, y=200)
            
            self.files_frame = CTkFrame(self.content, bg_color=THEME.PRIMARY_COLOR, fg_color=THEME.PRIMARY_COLOR_LIGHT, corner_radius=8)
            self.files_frame.pack(padx=20, pady=10, fill=BOTH, expand=True)

            header = CTkFrame(self.files_frame, fg_color=THEME.PRIMARY_COLOR_LIGHT, bg_color=THEME.PRIMARY_COLOR_LIGHT, height=40)
            header.pack(fill=X, padx=10, pady=(10, 0))
            h_name = CTkLabel(header, text="Dosya Adı", font=("Arial", 14, "bold"), text_color=THEME.TEXT_COLOR, bg_color=THEME.PRIMARY_COLOR_LIGHT)
            h_size = CTkLabel(header, text="Boyut", font=("Arial", 14, "bold"), text_color=THEME.TEXT_COLOR, bg_color=THEME.PRIMARY_COLOR_LIGHT)
            h_mtime = CTkLabel(header, text="Değiştirilme", font=("Arial", 14, "bold"), text_color=THEME.TEXT_COLOR, bg_color=THEME.PRIMARY_COLOR_LIGHT)
            h_name.place(relx=0.01, rely=0.5, anchor=W)
            h_size.place(relx=0.70, rely=0.5, anchor=W)
            h_mtime.place(relx=0.85, rely=0.5, anchor=W)

            rows_container = CTkScrollableFrame(self.files_frame, fg_color=THEME.PRIMARY_COLOR_LIGHT, bg_color=THEME.PRIMARY_COLOR_LIGHT, border_width=0, height=350)
            rows_container.pack(fill=BOTH, expand=True, padx=0, pady=(0,5))

            def _hr_size(num):
                for unit in ["B","KB","MB","GB","TB"]:
                    if num < 1024.0:
                        return f"{num:.1f} {unit}"
                    num /= 1024.0
                return f"{num:.1f} PB"

            files = []
            try:
                for entry in os.listdir(self.selectedFolder or ""):
                    full = os.path.join(self.selectedFolder, entry)
                    if os.path.isfile(full):
                        stat = os.stat(full)
                        files.append((entry, stat.st_size, stat.st_mtime, full))
            except Exception:
                files = []

            if not files:
                empty_lbl = CTkLabel(rows_container, text="Bu klasörde dosya bulunamadı.", font=("Arial", 14), text_color=THEME.TEXT_COLOR_RESERVE[1], bg_color=THEME.PRIMARY_COLOR)
                empty_lbl.pack(pady=20)
            else:
                files.sort(key=lambda x: x[0].lower())
                for i, (name, size, mtime, path) in enumerate(files):
                    row_color = THEME.PRIMARY_COLOR_LIGHT if (i % 2 == 0) else "#363636"
                    row = CTkFrame(rows_container, fg_color=row_color, bg_color=THEME.PRIMARY_COLOR, height=40, corner_radius=0, cursor="hand2")
                    row.pack(fill=X, pady=0, padx=2)

                    lbl_name = CTkLabel(row, text=name, anchor=W, font=("Arial", 13), text_color=THEME.TEXT_COLOR, bg_color=row_color)
                    lbl_size = CTkLabel(row, text=_hr_size(size), anchor=E, font=("Arial", 12), text_color=THEME.TEXT_COLOR, bg_color=row_color)
                    lbl_time = CTkLabel(row, text=datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M"), anchor=E, font=("Arial", 12), text_color=THEME.TEXT_COLOR, bg_color=row_color)

                    lbl_name.place(relx=0.01, rely=0.5, anchor=W)
                    lbl_size.place(relx=0.70, rely=0.5, anchor=W)
                    lbl_time.place(relx=0.85, rely=0.5, anchor=W)

                    def _open(p=path):
                        try:
                            if not os.path.exists(p):
                                mb.showerror("Hata", "Dosya bulunamadı.")
                                return
                            
                            if sys.platform.startswith("win"):
                                pnorm = os.path.normpath(p)
                                if os.path.isdir(pnorm):
                                    subprocess.Popen(['explorer', pnorm])
                                else:
                                    subprocess.Popen(['explorer', '/select,', pnorm])
                                    
                            elif sys.platform == "darwin":
                                if os.path.isdir(p):
                                    subprocess.Popen(['open', p])
                                else:
                                    subprocess.run(['open', '-R', p])
                                    
                            else:
                                target = p if os.path.isdir(p) else os.path.dirname(p)
                                subprocess.Popen(['xdg-open', target])
                        except Exception:
                            mb.showerror("Hata", "Dosya gezgininde gösterilemedi.")

                    row.bind("<Button-1>", lambda e, p=path: _open(p))
                    lbl_name.bind("<Button-1>", lambda e, p=path: _open(p))
                    lbl_size.bind("<Button-1>", lambda e, p=path: _open(p))
                    lbl_time.bind("<Button-1>", lambda e, p=path: _open(p))

                    def on_enter(e, widget=row):
                        widget.configure(fg_color=THEME.PRIMARY_COLOR_EXTRA_LIGHT)
                    def on_leave(e, widget=row, original=row_color):
                        widget.configure(fg_color=original)

                    row.bind("<Enter>", on_enter)
                    row.bind("<Leave>", on_leave)
                    lbl_name.bind("<Enter>", on_enter)
                    lbl_name.bind("<Leave>", on_leave)
                    lbl_size.bind("<Enter>", on_enter)
                    lbl_size.bind("<Leave>", on_leave)
                    lbl_time.bind("<Enter>", on_enter)
                    lbl_time.bind("<Leave>", on_leave)
            
    def start_org(self):
        state = organization(self.selectedFolder, self.isSpecialFolder.get())
        if state:
            mb.showinfo("Başarılı", "Dosyalar başarıyla organize edildi.")
            os.startfile(self.selectedFolder)

    def open_selected_folder(self):
        if self.selectedFolder:
            os.startfile(self.selectedFolder)


    def select_folder(self):
        folder_path = fd.askdirectory()
        if folder_path:
            self.process_files(folder_path)

    def process_files(self, folder_path):
        self.fileDirectoryEntry.configure(state=NORMAL)
        self.fileDirectoryEntry.delete(0, END)
        self.fileDirectoryEntry.insert(0, folder_path)
        self.fileDirectoryEntry.configure(state=DISABLED)
        
        self.selectedFolder = folder_path
        
        self.newStarted = False
                
        self.appContent()
        
def start():
    app = GUI()
    app.mainloop()
    
if __name__ == "__main__":
    start()