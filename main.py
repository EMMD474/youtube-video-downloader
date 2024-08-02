import customtkinter as c
from tkinter import ttk
import yt_dlp as tube
from yt_dlp.utils import DownloadError, DownloadCancelled
import threading
import time
from plyer import notification as n
import requests


class YoutubeDownloader(c.CTk):
    def __init__(self):
        super().__init__()

        self.title("Youtube Downloader")
        self.geometry("450x280")
        c.set_appearance_mode("dark")
        c.set_default_color_theme(r"C:\workstation\python\Themes\teal.json")

        self.main_frame = c.CTkFrame(self)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.switch_var = c.StringVar(value="on")
        self.switch = c.CTkSwitch(self.main_frame, text="Light / Dark Mode", variable=self.switch_var, onvalue='on',
                                  offvalue="off", command=self.change_mode)
        self.switch.pack(pady=10)

        self.entry = c.CTkEntry(self.main_frame, width=300, height=32, placeholder_text="URL", border_color="#035c5c")
        self.entry.pack(pady=10, padx=10)

        self.progress = ttk.Progressbar(self.main_frame, length=600)
        self.progress.pack(pady=10)

        self.btn_state = 'normal'
        self.btn = c.CTkButton(self.main_frame, text="Download", state=self.btn_state, command=self.start_download)
        self.btn.pack(pady=10, padx=10)

        self.display = c.CTkTextbox(self.main_frame, width=300)
        self.display.pack(pady=10, padx=10)

    def change_mode(self):
        if self.switch.get() == "off":
            c.set_appearance_mode("light")
        else:
            c.set_appearance_mode("dark")

    @staticmethod
    def check_internet_con():
        try:
            response = requests.get("https://www.google.com", timeout=5)
            print("Connection Established")
            return True
        except requests.ConnectionError:
            print("No Internet Connection")
            return False

    def start_download(self):
        if not self.check_internet_con():
            self.display.insert("end", "No Internet Connection!, \nTurn on WIFI! \n")
            self.entry.delete(0, "end")
        else:
            url: str = self.entry.get()

            if not url:
                self.display.insert("end", "URL can not be empty!")
            if url.startswith("https://"):
                threading.Thread(target=self.download, args=(url,)).start()
                self.btn_state = "disabled"
            else:
                self.display.insert("end", "input is not a url!")

    def download(self, url):
        try:
            yt = {
                "format": "best/bestvideo+bestaudio/best",
                "outtmpl": "~/Videos/YoutubeVideos/%(title)s.%(ext)s",
                "noplaylist": True,
                "progress_hooks": [self.progress_hook],
            }

            with tube.YoutubeDL({'listformats': True}) as ytd:
                formats = ytd.extract_info(url, download=False)
                print(formats)
            #
            # with tube.YoutubeDL(yt) as ytd:
            #     video_infor = ytd.extract_info(url, download=False)
            #     self.title = video_infor.get('title', None)
            #     self.display.insert("end", f"Beginning Download of {self.title}")
            #     ytd.download([url])
            #
            #     self.notify("Youtube Downloader", f"Download Complete! \n {self.title} has been downloaded")
            #     time.sleep(2)
            #     self.progress['value'] = 0
            #     self.main_frame.update_idletasks()
            #     self.entry.delete(0, "end")
        except DownloadError as e:
            print(f"[ERROR]: {e}")
            self.display.insert("end", "Download Error \n")
        except DownloadCancelled as e:
            self.display.insert("end", "Download Cancelled, Try Again. \n")
            print(f"[ERROR]: {e}")

    def progress_hook(self, d):
        if d['status'] == "downloading":
            total_bytes = d.get('total_bytes')
            downloaded_bytes = d.get("downloaded_bytes", 0)
            if total_bytes:
                percent = (downloaded_bytes / total_bytes) * 100
                self.progress['value'] = percent
                self.main_frame.update_idletasks()

    @staticmethod
    def notify(title, msg):
        n.notify(
            title=title,
            message=msg,
            app_name="Youtube Downloader"
        )


if __name__ == "__main__":
    app = YoutubeDownloader()
    app.mainloop()
    