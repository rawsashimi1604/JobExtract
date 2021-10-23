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
import processor
from tkinter import messagebox


class GUI:
    def __init__(self, window):
        self.window = window
        self.seniority_option = StringVar()
        self.clean_option = StringVar()
        self.job_str = StringVar()
        self.country_str = StringVar()
        self.number_str = StringVar()
        self.crawler_frame = tk.Frame()
        self.cleaner_frame = tk.Frame()
        self.crawler_open = False
        self.cleaner_open = False
        self.background_color = "#ADD8E6"

    def startGUI(self):
        window = self.window
        background_color = self.background_color
        self.seniority_option.set("All")
        self.clean_option.set("all")
        frame = tk.Frame(
            window,
            height=400,
            width=600,
            bg = background_color
        )
        frame2 = tk.Frame(
            frame,
            # width=600,
            # height=100,
            bg=background_color
        )
        frame3 =tk.Frame(
            frame,
            bg=background_color,
            width=600
        )
        greeting = tk.Label(
            frame2,
            text='Welcome to LinkedIn cleaner bot!',
            background= background_color,
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
        canvas.create_window((0, 0), window=status_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        crawl_button = tk.Button(
            frame2,
            text='Start Crawling Data!',
            background = "#cfcfcf",
            command= partial(self.crawlerGUI, frame3)
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
            command= partial(self.cleanerGUI,frame3)
        )
        pandas_button = tk.Button(
            frame2,
            text='Open Pandas excel file reader',
            background = "#cfcfcf",
            command = self.pandas_GUI
        )
        # Merge_button = tk.Button(
        #     frame7,
        #     text='Merge Data',
        #     background = "#cfcfcf",
        #     command= self.startMerging
        # )
        # count_button = tk.Button(
        #     frame7,
        #     text='Count data',
        #     background = "#cfcfcf",
        #     command=self.startCounting
        # )
        # augment_button = tk.Button(
        #     frame7,
        #     text='Augment Data',
        #     background = "#cfcfcf",
        #     command= self.startAugmenting
        # )
        # clear_button = tk.Button(
        #     frame7,
        #     text='Clear All Input',
        #     background = "#cfcfcf",
        #     command=partial(self.clear_all,input_job,input_country,self.option,input_number)
        # )
        frame.place(relx=0.1, relwidth=0.8, relheight=0.9)
        frame2.pack(side='top',pady=5)
        frame3.pack(side='top',pady=10)
        greeting.pack(pady=10)
        crawl_button.pack(side='left',padx=10,pady=5)
        clean_button.pack(side='left',padx=10,pady=5)
        pandas_button.pack(side='left',padx=10,pady=5)
        github_button.pack(side='left',padx=10,pady=5)
        # Merge_button.pack(side='left',padx=10,pady=5)
        # count_button.pack(side='left',padx=10,pady=5)
        # augment_button.pack(side='left',padx=10,pady=5)
        # clear_button.pack(side='left',padx=10,pady=5)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        # startCrawling = partial(self.startCrawler,job_str,country_str,option,number_str)
        window.mainloop()
    
    def crawlerGUI(self,parent_frame):
        if self.crawler_open:
            self.crawler_open = False
            parent_frame.configure(height=0)
            self.destroy_frame(self.crawler_frame)
        else:
            background_color = self.background_color
            crawl_number = self.number_str
            self.crawler_open = True
            if self.cleaner_open:
                self.cleaner_open = False
                self.destroy_frame(self.cleaner_frame)
            self.crawler_frame=tk.Frame(
                parent_frame,
                background=background_color
            )
            lbljobs = tk.Label(
                self.crawler_frame,
                text='Enter Job: ',
                background= background_color
            )
            input_job = tk.Entry(
                self.crawler_frame,
                font=30,
                textvariable=self.job_str
            )
            lblcountry = tk.Label(
                self.crawler_frame,
                text='Enter Country: ',
                background= background_color
            )
            input_country = tk.Entry(
                self.crawler_frame,
                font=30,
                textvariable=self.country_str
            )
            lbllevel = tk.Label(
                self.crawler_frame,
                text='Pick a Seniority Level: ',
                background=background_color
            )
            rb_all = tk.Radiobutton(
                self.crawler_frame,
                text="All",
                background= background_color,
                activebackground=background_color,
                value="All",
                var=self.seniority_option
            )
            rb_associate = tk.Radiobutton(
                self.crawler_frame,
                text="Associate",
                background= background_color,
                activebackground=background_color,
                value="Associate",
                var=self.seniority_option
            )
            rb_director = tk.Radiobutton(
                self.crawler_frame,
                text="Director",
                background= background_color,
                activebackground=background_color,
                value="Director",
                var=self.seniority_option
            )
            rb_entry = tk.Radiobutton(
                self.crawler_frame,
                text="Entry",
                background= background_color,
                activebackground=background_color,
                value="Entry",
                var=self.seniority_option
            )
            rb_internship = tk.Radiobutton(
                self.crawler_frame,
                text="Internship",
                background= background_color,
                activebackground=background_color,
                value="Internship",
                var=self.seniority_option

            )
            rb_mid_senior = tk.Radiobutton(
                self.crawler_frame,
                text="Mid-Senior",
                background= background_color,
                activebackground=background_color,
                value="Mid-Senior",
                var=self.seniority_option
            )
            lblnumber = tk.Label(
                self.crawler_frame,
                text='Please enter the number of data to be crawled:',
                background= background_color
            )
            entry_number = tk.Entry(
                self.crawler_frame,
                font=30,
                textvariable=crawl_number,
                width=1
            )
            input_number = tk.Scale(
                self.crawler_frame,
                font=30,
                orient="horizontal",
                variable=crawl_number,
                from_=1,
                to=1000,
                showvalue=0,
                highlightbackground=background_color,
                relief="sunken"
                # textvariable=self.number_str
            )
            startCrawl_button = tk.Button(
                self.crawler_frame,
                text="Start crawling",
                state="disabled",
                command=self.startCrawler
            )
            self.crawler_frame.pack(side='left')
            self.job_str.trace_add("write", partial(self.validate_crawl, startCrawl_button))
            self.country_str.trace_add("write", partial(self.validate_crawl, startCrawl_button))
            lbljobs.grid(row=0,column=0,sticky="W")
            input_job.grid(row=0,column=1,padx=(0,15),columnspan=3,sticky="W")
            lblcountry.grid(row=0,column=3,padx=(15,0))
            input_country.grid(row=0,column=4,columnspan=3)
            lbllevel.grid(row=1,column=0,sticky='W')
            rb_all.grid(row=1,column=1,sticky='W')
            rb_associate.grid(row=1,column=2,sticky='W')
            rb_director.grid(row=1,column=3,sticky='W')
            rb_entry.grid(row=1,column=4,sticky='W')
            rb_internship.grid(row=2,column=1,sticky='W')
            rb_mid_senior.grid(row=2,column=2,sticky='W')
            lblnumber.grid(row=3,column=0,sticky='W',columnspan=2)
            entry_number.grid(row=3,column=2,sticky='EW',padx=5)
            input_number.grid(row=3,column=3,sticky="EW", columnspan=4)
            startCrawl_button.grid(row=4,column=0, columnspan=8,pady=(10,0))
            
    def cleanerGUI(self,parent_frame):
        if self.cleaner_open:
            self.cleaner_open = False
            parent_frame.configure(height=0)
            self.destroy_frame(self.cleaner_frame)
        else:
            background_color = self.background_color
            self.cleaner_open = True
            if self.crawler_open:
                self.crawler_open = False
                self.destroy_frame(self.crawler_frame)
            self.cleaner_frame=tk.Frame(
                parent_frame,
                width=600,
                background=background_color,
            )
            lbl_processing_mode = tk.Label(
                self.cleaner_frame,
                text='Select processing mode mode: ',
                background=background_color
            )
            rb_all = tk.Radiobutton(
                self.cleaner_frame,
                text="All: Processes all files in all rawData directories",
                background= background_color,
                activebackground=background_color,
                value="all",
                var=self.clean_option
            )
            rb_latestAll = tk.Radiobutton(
                self.cleaner_frame,
                text="All Latest: Processes latest files in all rawData directories",
                background= background_color,
                activebackground=background_color,
                value="latestAll",
                var=self.clean_option
            )
            rb_single = tk.Radiobutton(
                self.cleaner_frame,
                text="Single: Processes single file",
                background= background_color,
                activebackground=background_color,
                value="single",
                var=self.clean_option,
            )
            clean_button = tk.Button(
                self.cleaner_frame,
                text="Clean file",
                command=self.startCleaner
            )
            self.cleaner_frame.pack(side='left')
            lbl_processing_mode.grid(row=0,column=0,sticky='W')
            rb_all.grid(row=1,column=0,sticky='W')
            rb_latestAll.grid(row=2,column=0,sticky='W')
            rb_single.grid(row=3,column=0,sticky='W')
            clean_button.grid(row=4,column=0, sticky='W')

    def destroy_frame(self,frame):
        frame.destroy()            

    def validate_crawl(self,*args):
        job_str = self.job_str.get()
        country_str = self.country_str.get()
        if job_str:
            if country_str:
                args[0].config(state="normal")
            else:
                args[0].config(state="disabled")
        else:
            args[0].config(state="disabled")

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

    def startCleaner(self):
        clean_option = self.clean_option.get()
        if clean_option == "single":
            filename = ''
            filename = self.chooseDirectory()
            myProcessor = processor.Processor(format=clean_option,manualFilePath=filename)
        else:
            myProcessor  = processor.Processor(format=clean_option)
        myProcessor.process()
        # try:
        #     filename = self.chooseDirectory()
        #     myCleaner = cleaner.Cleaner()
        #     myCleaner.startCleaner(filename)
        #     cleaning_text = 'Successfully cleaned {}'.format(filename)
        #     cleaning_status = tk.Label(
        #         status_frame,
        #         text=cleaning_text,
        #         fg='green',
        #         wraplength=550,
        #         justify='left'
        #     )
        #     cleaning_status.pack(side='top')
        #     cleaned_filename = myCleaner.makeCleanedDataFileDirectory(filename)
        #     df = pd.read_csv(cleaned_filename)
        #     self.pandas_GUI(df)
        #     # status_text.insert('1.0', cleaning_text)
        # except (KeyError, AttributeError) as e:
        #     if len(filename) > 0:
        #         error_status = tk.Label(
        #             status_frame,
        #             text= 'Error when cleaning file {}'.format(filename),
        #             fg = 'red',
        #             wraplength=550,
        #             justify='left'
        #         )
        #         error_status.pack(side='top')
        #     print(e)
        
    def startCrawler(self):
        job_get = (self.job_str.get())
        country_get = (self.country_str.get())
        level_get = (self.seniority_option.get())
        amount_get = (self.number_str.get())
        if not job_get.isalpha():
            messagebox.showerror("Enter Job input error!!","Please enter a job in letters only.")
            job.delete(0,END)
        elif not country_get.isalpha():
            messagebox.showerror("Enter country input error!!","Please enter a country in letters only.")
            country.delete(0,END)
        else:
            myCrawler = crawler.Crawler()
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
    window = tk.Tk()
    window.title("LinkedIn Data Cleaner")
    window.configure(background='#ADD8E6', pady = "20", padx ="10", height= 600, width=800)
    myGUI = GUI(window)
    myGUI.startGUI()
    