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
import merger
import counter
import augmentor


class GUI:
    def __init__(self):
        pass

    def startGUI(self):
        window = tk.Tk()
        window.title("LinkedIn Data Cleaner")
        window.configure(background='#ADD8E6', pady = "20", padx ="10", height= 600, width=800)
        option = StringVar()
        job_str = StringVar()
        country_str = StringVar()
        number_str = StringVar()
        option.set("All")
        
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
        frame3 =tk.Frame(
            frame,
            bg="#ADD8E6"
        )
        frame4 =tk.Frame(
            frame,
            bg="#ADD8E6"
        )
        frame5 =tk.Frame(
            frame,
            bg="#ADD8E6"
        )
        frame6 =tk.Frame(
            frame,
            bg="#ADD8E6"
        )
        frame7 =tk.Frame(
            frame,
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
            frame6,
            text='Start Crawling Data!',
            background = "#cfcfcf",
            command= partial(self.startCrawler,job_str,country_str,option,number_str)
        )
        github_button = tk.Button(
            frame6,
            text='GitHub',
            background = "#cfcfcf",
            command= partial(self.Open_git_Url)
        )
        clean_button = tk.Button(
            frame6,
            text='Clean data file',
            background = "#cfcfcf",
            command= partial(self.startCleaner,status_frame)
        )
        # for i in range (50):
        #     tk.Label(status_frame, text="Sample scrolling label").pack()
        pandas_button = tk.Button(
            frame6,
            text='Open Pandas excel file reader',
            background = "#cfcfcf",
            command = self.pandas_GUI
        )
        lbljobs = tk.Label(
            frame2,
            text='Enter Job: ',
            background= "#ADD8E6"
        )
        input_job = tk.Entry(
            frame2,
            font=30,
            textvariable=job_str
            
        )
        lblcountry = tk.Label(
            frame2,
            text='Enter Country: ',
            background= "#ADD8E6"
        )
        input_country = tk.Entry(
            frame2,
            font=30,
            textvariable=country_str
        )
        lbllevel = tk.Label(
            frame3,
            text='Pick a Seniority Level: ',
            background="#ADD8E6"
        )
        rb_all = tk.Radiobutton(
            frame4,
            text="All",
            background= "#ADD8E6",
            value="All",
            var=option
        )
        rb_associate = tk.Radiobutton(
            frame4,
            text="Associate",
            background= "#ADD8E6",
            value="Associate",
            var=option
        )
        rb_director = tk.Radiobutton(
            frame4,
            text="Director",
            background= "#ADD8E6",
            value="Director",
            var=option
        )
        rb_entry = tk.Radiobutton(
            frame4,
            text="Entry",
            background= "#ADD8E6",
            value="Entry",
            var=option
        )
        rb_internship = tk.Radiobutton(
            frame4,
            text="Internship",
            background= "#ADD8E6",
            value="Internship",
            var=option

        )
        rb_mid_senior = tk.Radiobutton(
            frame4,
            text="Mid-Senior",
            background= "#ADD8E6",
            value="Mid-Senior",
            var=option
        )
        lblnumber = lbllevel = tk.Label(
            frame5,
            text='Please enter the number of data to be crawled:',
            background= "#ADD8E6"
        )
        input_number = tk.Entry(
            frame5,
            font=30,
            textvariable=number_str
        )
        Merge_button = tk.Button(
            frame7,
            text='Merge Data',
            background = "#cfcfcf",
            command= self.startMerging
        )
        count_button = tk.Button(
            frame7,
            text='Count data',
            background = "#cfcfcf",
            command=self.startCounting
        )
        augment_button = tk.Button(
            frame7,
            text='Augment Data',
            background = "#cfcfcf",
            command= self.startAugmenting
        )
        clear_button = tk.Button(
            frame7,
            text='Clear All Input',
            background = "#cfcfcf",
            command=partial(self.clear_all,input_job,input_country,option,input_number)
        )



        frame2.pack(side='top',pady=5)
        frame3.pack(side='top',pady = 10)
        frame4.pack(side='top')
        frame5.pack(side='top')
        frame6.pack(side='top')
        frame7.pack(side='top')
        frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
        # rb_associate.deselect()
        # rb_director.deselect()
        # rb_entry.deselect()
        # rb_internship.deselect()
        # rb_mid_senior.deselect()
        
        greeting.pack(pady=10)
        lbljobs.pack(side='left')
        input_job.pack(side='left',padx=10)
        lblcountry.pack(side="left")
        input_country.pack(side='left',padx=10)
        # lbllevel.pack(pady=10) this label refuse to appear
        rb_all.pack(side='left',padx=10)
        rb_associate.pack(side='left',padx=10)
        rb_director.pack(side='left',padx=10)
        rb_entry.pack(side='left',padx=10)
        rb_internship.pack(side='left',padx=10)
        rb_mid_senior.pack(side='left',padx=10)
        lblnumber.pack(side='left')
        input_number.pack(side='left',padx=10)

        # pandas_button.pack()
        clean_button.pack(side='left',padx=10,pady=5)
        pandas_button.pack(side='left',padx=10,pady=5)
        crawl_button.pack(side='left',padx=10,pady=5)
        github_button.pack(side='left',padx=10,pady=5)
        Merge_button.pack(side='left',padx=10,pady=5)
        count_button.pack(side='left',padx=10,pady=5)
        augment_button.pack(side='left',padx=10,pady=5)
        clear_button.pack(side='left',padx=10,pady=5)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        # startCrawling = partial(self.startCrawler,job_str,country_str,option,number_str)
        window.mainloop()

    def chooseDirectory(self):
        cwd = getcwd()
        filename = tk.filedialog.askopenfile(initialdir=cwd, title="Select Data File", filetypes=(("CSV files","*.csv"),("all files","*.*"))).name
        return filename
        # self.filename = tk.filedialog.askopenfile(initialdir=cwd, title="Select Data File", filetypes=(("CSV files","*.csv"),("all files","*.*"))).name
        # self.startCleaner()
    def startMerging(self):
        filename = self.chooseDirectory()
        myMerger = merger.Merger()
        merge_all = myMerger.merging_all_files(*filename)
        myMerger.createNewFile(merge_all,"New_Merge_file")
    
    def startCounting(self):
        filename = self.chooseDirectory()
        myCounter = counter.Counter()
        myCounter.exportToCSV(filename)

    def startAugmenting(self):
        filename = self.chooseDirectory()
        myAugmentor = augmentor.Augmentor(filename)
        myAugmentor.augment()



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
        
    def startCrawler(self,job,country,level,amount):
        myCrawler = crawler.Crawler()
        job_get = (job.get())
        country_get = (country.get())
        level_get = (level.get())
        amount_get = (amount.get())
        myCrawler.startCrawler(job_get, country_get, level_get, int(amount_get))
    
    def clear_all(self, job,country,level,amount):
        job.delete(0,END)
        country.delete(0,END)
        level.set("All")
        amount.delete(0,END)

        #os.system("py ../controller/crawler.py")
    # def get_job(self):
    #     job = input_job.get(1.0, "end-1c")
    #     print(job)
    # def get_country(self):
    #     country = input_country.get(1.0, "end-1c")
    #     print(country)
    # def get_number(self):
    #     number = int(input_number.get(1.0, "end-1c"))
    #     print(number)




    def pandas_GUI(self, df =''):
        show(df)

    def Open_git_Url(self):
        webbrowser.open_new("https://github.com/rawsashimi1604/1002_LinkedIn")

if __name__ == "__main__":
    myGUI = GUI()
    myGUI.startGUI()
    