import os, shutil

def organization(folder_path, isSpecial):
    try:
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        file_types = {
            "Resim": [
                ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif",
                ".svg", ".webp", ".heif", ".heic", ".ico", ".raw"
            ],
            "Video": [
                ".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm",
                ".mpeg", ".mpg", ".3gp", ".vob", ".ogv", ".m4v"
            ],
            "Doküman": [
                ".pdf", ".doc", ".docx", ".txt", ".odt", ".rtf", ".tex",
                ".xls", ".xlsx", ".csv", ".ppt", ".pptx", ".odp", ".ods"
            ],
            "Ses": [
                ".mp3", ".wav", ".aac", ".ogg", ".flac", ".wma", ".m4a",
                ".amr", ".aiff", ".opus", ".mid", ".midi"
            ],
            "Uygulama": [
                ".exe", ".msi", ".apk", ".bat", ".sh", ".lnk", ".deb",
                ".rpm", ".appimage", ".jar", ".com"
            ],
            "Yazılım": [
                ".js", ".ts", ".json", ".py", ".html", ".htm", ".css",
                ".c", ".cpp", ".cs", ".java", ".php", ".swift", ".go",
                ".rb", ".kt", ".rs", ".pl", ".lua", ".sh", ".sql", ".r",
                ".ipynb", ".yml", ".yaml", ".xml", ".vue", ".dart"
            ],
            "Sıkıştırılmış": [
                ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz",
                ".iso", ".cab", ".lz", ".lzma", ".zst"
            ],
            "Veritabanı": [
                ".db", ".sqlite", ".sqlite3", ".mdb", ".accdb", ".sql",
                ".dbf", ".frm", ".ibd", ".ndf", ".ldf"
            ],
            "Font": [
                ".ttf", ".otf", ".woff", ".woff2", ".eot"
            ]
        }

        for file in files:
            file_ext = os.path.splitext(file)[1].lower()
            moved = False

            for category, extensions in file_types.items():
                if file_ext in extensions:
                    target_dir = os.path.join(folder_path, category)
                    if not os.path.exists(target_dir):
                        os.makedirs(target_dir)
                    shutil.move(os.path.join(folder_path, file), os.path.join(target_dir, file))
                    moved = True
                    break
            
            if not moved and isSpecial:
                special_dir = os.path.join(folder_path, "Özel")
                if not os.path.exists(special_dir):
                    os.makedirs(special_dir)
                shutil.move(os.path.join(folder_path, file), os.path.join(special_dir, file))
    
    except Exception as e:
        print("Hata:", e)
        return False
    
    return True
