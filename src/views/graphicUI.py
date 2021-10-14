import tkinter as tk
from os import getcwd
from functools import partial
import sys
import pandas as pd
from pandasgui import show
sys.path.append('../controller')
import cleaner
from tkinter import *
import webbrowser
import crawler
import os


class GUI:
    def __init__(self):
        pass

    def startGUI(self):
        window = tk.Tk()
        window.title("LinkedIn Data Cleaner")
        window.configure(background='#ADD8E6', pady = "20", padx ="10", height= 600, width=800)
        frame = tk.Frame(
            window,
            height=400,
            width=600,
            bg = "#ADD8E6"
        )
        frame2 = tk.Frame(
            frame,
            # width=600,
            # height=100,
            bg="#ADD8E6"
        )
        greeting = tk.Label(
            frame2,
            text='Welcome to LinkedIn cleaner bot!',
            background= "#ADD8E6",
        )
        
        canvas = tk.Canvas(
            frame,
        )
        scrollbar = tk.Scrollbar(
            frame,
            orient='vertical',
            command=canvas.yview,
        )
        status_frame = tk.Frame(
            canvas,
            height=350,
            width=450,
        )
        status_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        # pandas_button = tk.Button(
        #     frame,
        #     text= "open pandas",
        #     command=show
        # )
        canvas.create_window((0, 0), window=status_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        crawl_button = tk.Button(
            frame2,
            text='Start Crawling Data!',
            background = "#cfcfcf",
            command= partial(self.startCrawler)
        )
        github_button = tk.Button(
            frame2,
            text='GitHub',
            background = "#cfcfcf",
            command= partial(self.Open_git_Url)
        )
        clean_button = tk.Button(
            frame2,
            text='Clean data file',
            background = "#cfcfcf",
            command= partial(self.startCleaner,status_frame)
        )
        # for i in range (50):
        #     tk.Label(status_frame, text="Sample scrolling label").pack()
        pandas_button = tk.Button(
            frame2,
            text='Open Pandas excel file reader',
            background = "#cfcfcf",
            command = self.pandas_GUI
        )
        frame2.pack(side='top')
        frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
        
        greeting.pack()
        # pandas_button.pack()
        clean_button.pack(side='left',padx=10)
        pandas_button.pack(side='left',padx=10)
        crawl_button.pack(side='left',padx=10)
        github_button.pack(side='left',padx=10)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        window.mainloop()

    def chooseDirectory(self):
        cwd = getcwd()
        filename = tk.filedialog.askopenfile(initialdir=cwd, title="Select Data File", filetypes=(("CSV files","*.csv"),("all files","*.*"))).name
        return filename
        # self.filename = tk.filedialog.askopenfile(initialdir=cwd, title="Select Data File", filetypes=(("CSV files","*.csv"),("all files","*.*"))).name
        # self.startCleaner()

    def startCleaner(self,status_frame):
        filename = ''
        try:
            filename = self.chooseDirectory()
            myCleaner = cleaner.Cleaner()
            myCleaner.startCleaner(filename)
            cleaning_text = 'Successfully cleaned {}'.format(filename)
            cleaning_status = tk.Label(
                status_frame,
                text=cleaning_text,
                fg='green',
                wraplength=550,
                justify='left'
            )
            cleaning_status.pack(side='top')
            cleaned_filename = myCleaner.makeCleanedDataFileDirectory(filename)
            df = pd.read_csv(cleaned_filename)
            self.pandas_GUI(df)
            # status_text.insert('1.0', cleaning_text)
        except (KeyError, AttributeError) as e:
            if len(filename) > 0:
                error_status = tk.Label(
                    status_frame,
                    text= 'Error when cleaning file {}'.format(filename),
                    fg = 'red',
                    wraplength=550,
                    justify='left'
                )
                error_status.pack(side='top')
            print(e)
        
    def startCrawler(self):
        # MyCrawler = crawler.Crawler()
        # MyCrawler.searchJobs("Sales", "Singapore")
        # myCrawler.selectPositionLevel("Associate")
        # myCrawler.getJobInfo(1000)
        os.system("py ../controller/crawler.py")



    def pandas_GUI(self, df =''):
        show(df)

    def Open_git_Url(self):
        webbrowser.open_new("https://github.com/rawsashimi1604/1002_LinkedIn")

if __name__ == "__main__":
    myGUI = GUI()
    myGUI.startGUI()
    