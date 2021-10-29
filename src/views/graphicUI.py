import tkinter as tk
from os import getcwd
from functools import partial
import sys
import pandas as pd
from pandasgui import show
from datetime import datetime
sys.path.append('../controller')
from tkinter import *
import webbrowser
import crawler
import os
from cleaner import Cleaner
from merger import Merger
from counter import Counter
from augmentor import Augmentor
from tkinter import messagebox

"""
    GUI Module. Contains the GUI Object to display the Graphical User Interface that integrates all the functionalities
    of the program and allows the users to access it all in one place
"""
class GUI:
    '''
        GUI Object

        Class Attributes:
            window: tk.Tk() => The window in which the GUI is built on
            log_text: tk.Text() => The text object which will be displayed in the log. Can be modified with 
            seniortity_option: StringVar() => The seniority value that to be inputted into the crawler
            job_str: StringVar() => The job string to be inputted into the crawler
            number_str: StringVar() => The number of jobs to be crawled by the crawler
            clean_option: StringVar() => The clean option to be inputted into the cleaner
            crawler_frame: tk.Frame() => The frame containing the crawler input options
            cleaner_frame: tk.Frame() => The frame containing the cleaner input options
            crawler_open: bool => Boolean value dictating whether the crawler options is to be displayed
            cleaner_open: bool => Boolean value dictating whether the cleaner options is to be displayed
            background_color: str => String value of a hex color to define what the background color is for all elements in the GUI
            success_tag: str => String value to be passed into the write_log function to display a green text
            error_tag: str => String value to be passed into the write_log function to display a red text
            manualFilePath: str => Specifies path for "single" format processing.
            files: List => List of files to be processed
            mergedFilepath: str => Specifies path for augmenting.
    '''
    def __init__(self, window):
        ''' 
            Constructor for GUI Class.
            Parameters:
                window: tk.Tk() => Defines the tkinter window to display the GUI in
            Returns:
                GUI => Constructs GUI Class
        '''
        self.window = window
        self.log_text = tk.Text()
        self.seniority_option = StringVar()
        self.job_str = StringVar()
        self.country_str = StringVar()
        self.number_str = StringVar()
        self.clean_option = StringVar()
        self.crawler_frame = tk.Frame()
        self.cleaner_frame = tk.Frame()
        self.crawler_open = False
        self.cleaner_open = False
        self.background_color = "#ADD8E6"
        self.success_tag = "success"
        self.error_tag = "error"
        self.manualFilePath = ''
        self.files = []
        self.mergedFilePath = ""

    def startGUI(self):
        '''
            Start the GUI and display all the main page elements.
            Parameters:
                None
            Returns:
                None
        '''
        window = self.window
        background_color = self.background_color
        self.seniority_option.set("All")
        self.clean_option.set("all")
        jobExtract_logo = PhotoImage(file="../../images/jobExtractLogo.png")
        jobExtract_logo_resized = jobExtract_logo.subsample(1,1)
        github_logo = PhotoImage(file="../../images/github-logo.png")
        github_logo_resized = github_logo.subsample(30,40)
        frame = tk.Frame(
            window,
            bg = background_color,
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
            image=jobExtract_logo_resized
        )
        canvas = tk.Canvas(
            frame,
        )
        scrollbar = tk.Scrollbar(
            frame,
            orient='vertical',
            command=canvas.yview,
        )
        log_frame = tk.Frame(
            canvas,
        )
        self.log_text = tk.Text(
            log_frame,
            state=DISABLED,
            padx=5
        )
        self.log_text.tag_config('black', foreground="black")
        self.log_text.tag_config('success', foreground="green")
        self.log_text.tag_config("error", foreground="red")
        log_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=log_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        crawl_button = tk.Button(
            frame2,
            text='Start Crawling Data!',
            background = "#cfcfcf",
            command= partial(self.crawlerGUI, frame3)
        )
        github_button = tk.Button(
            frame2,
            text=' GitHub',
            background = "#cfcfcf",
            command= partial(self.Open_git_Url),
            image=github_logo_resized,
            compound="left"
        )
        clean_button = tk.Button(
            frame2,
            text='Clean Data File',
            background = "#cfcfcf",
            command= partial(self.cleanerGUI,frame3)
        )
        count_button = tk.Button(
            frame2,
            text='Count Data',
            background= "#cfcfcf",
            command=self.startCounting
        )
        pandas_button = tk.Button(
            frame2,
            text='Open Pandas Excel File Reader',
            background = "#cfcfcf",
            command = self.pandas_GUI
        )
        frame.place(relx=0.1, relwidth=0.8, relheight=0.9)
        frame2.pack(side='top',pady=5)
        frame3.pack(side='top',pady=10)
        greeting.pack(side='top',pady=10)
        crawl_button.pack(side='left',padx=10,pady=5)
        clean_button.pack(side='left',padx=10,pady=5)
        count_button.pack(side='left',padx=10,pady=5)
        pandas_button.pack(side='left',padx=10,pady=5)
        github_button.pack(side='left',padx=10,pady=5)
        canvas.pack(side="left", fill="both", expand=True)
        self.log_text.pack(side='top')
        scrollbar.pack(side="right", fill="y")
        window.mainloop()

    def crawlerGUI(self,parent_frame):
        '''
            Display the crawler GUI to collect the parameters to be passed to the startCrawler function.
            Parameters:
                parent_frame: tk.Frame() => The parent frame where the crawler GUI is to be displayed
            Returns:
                None
        '''
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
            input_job.grid(row=0,column=1,padx=(0,15),columnspan=2,sticky="W")
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
            input_number.grid(row=3,column=3,sticky="EW", columnspan=3)
            startCrawl_button.grid(row=4,column=0, columnspan=8,pady=(10,0))
            
    def cleanerGUI(self,parent_frame):
        '''
            Display the cleaner GUI to collect the parameters to be passed to the startCleaner function.
            Parameters:
                parent_frame: tk.Frame() => The parent frame where the crawler GUI is to be displayed
            Returns:
                None
        '''
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
                command=self.processFiles
            )
            self.cleaner_frame.pack(side='left')
            lbl_processing_mode.grid(row=0,column=0,sticky='W')
            rb_all.grid(row=1,column=0,sticky='W')
            rb_latestAll.grid(row=2,column=0,sticky='W')
            rb_single.grid(row=3,column=0,sticky='W')
            clean_button.grid(row=4,column=0, sticky='W')

    def destroy_frame(self,frame):
        '''
            Destroy the frame passed into it.
            Parameters:
                frame: tk.Frame() => The Tkinter frame to be destroyed
            Returns:
                None
        '''
        frame.destroy()            

    def validate_crawl(self,*args):
        '''
            Function to validate the crawler input boxes, and disable the start crawl button accordingly
            Parameters:
                *args: List => List of objects passed by the listener attached to the input boxes of the crawler GUI
            Returns:
                None
        '''
        job_str = self.job_str.get()
        country_str = self.country_str.get()
        if job_str:
            if country_str:
                args[0].config(state="normal")
            else:
                args[0].config(state="disabled")
        else:
            args[0].config(state="disabled")

    def write_log(self,text, tag='black'):
        '''
            Function to write text into the log canvas.
            Parameters:
                text: str => Text to be displayed in the logs
                tag: str (Optional) => Tag attached to it. ("Success" = green text, "Error" = red text, default is black text)
            Returns:
                None
        '''
        self.log_text.configure(state=NORMAL)
        if self.log_text.get("1.0","end-2c") == "":
            self.log_text.insert(INSERT,text,tag)
        else:
            self.log_text.insert(END,"\n"+text,tag)
        self.log_text.configure(state=DISABLED)

    def chooseDirectory(self):
        '''
            Open the file dialog for the user to choose the data file and updates the manualFilePath variable
            Parameters:
                None:
            Returns:
                None
        '''
        cwd = os.getcwd
        filename = tk.filedialog.askopenfile(initialdir=cwd, title="Select Data File", filetypes=(("CSV files","*.csv"),("all files","*.*"))).name
        self.manualFilePath = filename

    def processFiles(self) -> None:
        '''
            Main function, cleans files according to format class attribute, merges them together, then augments data points, saving it to a new file.
            Parameters:
                None
            Returns:
                None
        '''
        self.cleanFiles()
        self.mergeFiles()
        self.augmentFile()
        self.write_log("Cleaning has ended.")
    
    @staticmethod
    def dateTime() -> str:
        '''
            Returns today's date and time
            Parameters:
                None
            Returns:
                str => Formatted string containing date and time.
        '''
        now = datetime.now()
        datetime_string = now.strftime("%Y_%m_%d_%H_%M")

        return datetime_string

    def cleanFiles(self) -> None:
        '''
            Cleans all files according to specified format attribute, adds cleaned files into class attributes to be accessed by other functions.
            Parameters:
                None
            Returns:
                None
        '''
        self.write_log(f"Format selected is {self.clean_option.get()}. Cleaning will begin now...")
        window.update()

        myCleaner = Cleaner()
        
        # Get all files to clean
        searchPath = "../data/rawData"
        countries = os.listdir(searchPath)
        positions = ["Associate", "Director", "Entry", "Internship", "Mid-Senior"]

        if self.clean_option.get()== "single":
            self.chooseDirectory()
            if self.manualFilePath:
                # self.manualFilePath = self.manualFilePath.encode('unicode_escape')
                self.files.append(self.manualFilePath)
                myCleaner.startCleaner(self.manualFilePath)
                newPath = self.manualFilePath.replace("rawData", "cleanedData")
                self.write_log(f"Cleaned {self.manualFilePath}\nCleaning successful.\nCleaned Data saved @ \n{newPath}\n",self.success_tag)
                window.update()
                self.files.append(newPath)
            else:
                self.write_log(f"Error when cleaning file. Please try again.", self.error_tag)
                raise ValueError("manualFilePath attribute cannot be empty when selecting single format")
        
        for country in countries:
            for position in positions:
                currPath = fr"{searchPath}/{country}/{position}"
                currPathFiles = os.listdir(currPath)
                if self.clean_option.get() == "all":
                    if len(currPathFiles) != 0:
                        for file in currPathFiles:
                            filePath = fr"{currPath}/{file}"
                            myCleaner.startCleaner(filePath)
                            newPath = filePath.replace("rawData", "cleanedData")
                            self.write_log(f"Cleaned {file} @ \n{filePath}\nCleaning successful.\nCleaned Data saved @ \n{newPath}\n",self.success_tag)
                            window.update()
                            self.files.append(newPath)

                elif self.clean_option.get() == "latestAll":
                    if len(currPathFiles) != 0:
                        # Get latest file
                        file = currPathFiles[-1]
                        filePath = fr"{currPath}/{file}"
                        newPath = filePath.replace("rawData", "cleanedData")
                        myCleaner.startCleaner(filePath)
                        self.write_log(f"Cleaned {file} @ \n{filePath}\nCleaning successful.\nCleaned Data saved @ \n{newPath}\n",self.success_tag)
                        window.update()
                        self.files.append(newPath)

                elif self.clean_option.get() == "single":
                    pass

                else: 
                    self.write_log("Error when cleaning file. Please try again.", self.error_tag)
                    raise ValueError("Please enter a correct format value")

    def mergeFiles(self) -> None:
        '''
            Merges all files according to specified format attribute, adds merged file path into class attributes to be accessed by other functions.
            Parameters:
                None
            Returns:
                None
        '''
        myMerger = Merger()
        self.write_log("Merging in progress...")
        window.update()
        mergedDf = myMerger.merging_all_files(*self.files)
        mergedFileName = fr"{self.dateTime()}_MERGED"
        myMerger.createNewFile(mergedDf, mergedFileName)
        self.mergedFilePath = fr"../data/mergedData/{mergedFileName}.csv"
        self.write_log(f"Successfully merged file @\n{self.mergedFilePath}",self.success_tag)
        window.update()
    
    def augmentFile(self) -> None:
        '''
            Augments merged file.
            Parameters:
                None
            Returns:
                None
        '''
        self.write_log("Augmenting in progress...")
        window.update()
        myAugmentor = Augmentor(self.mergedFilePath)
        augmentedFilePath = self.mergedFilePath.replace("mergedData", "augmentedData").replace("MERGED", "AUGMENTED")
        myAugmentor.augment()
        self.write_log(f"Successfully augmented file @\n{augmentedFilePath}\n",self.success_tag)
        window.update()

    def startCounting(self):
        '''
            Starts the counting process on the data file
            Parameters:
                None
            Returns:
                None
        '''
        self.chooseDirectory()
        self.write_log("Counting data. Please wait")
        window.update()
        try:
            myCounter = Counter()
            myCounter.exportToCSV(self.manualFilePath)
            self.write_log("Successfully counted data. Data saved at " + myCounter.getExportLocation(self.manualFilePath), self.success_tag)
        except Exception as e:
            print(e)
            self.write_log("Error counting file. Please try again.", self.error_tag)

    def startCrawler(self):
        '''
            Starts the crawling process with the input variables from crawler GUI
            Parameters:
                None
            Returns:
                None
        '''
        job_get = (self.job_str.get())
        country_get = (self.country_str.get())
        level_get = (self.seniority_option.get())
        amount_get = (self.number_str.get())
        if not all(c.isalpha() or c.isspace() for c in job_get):
            messagebox.showerror("Enter Job input error!!","Please enter a job in letters only.")
        elif not all(c.isalpha() or c.isspace() for c in country_get):
            messagebox.showerror("Enter country input error!!","Please enter a country in letters only.")
        else:
            try:
                self.write_log("Starting crawler...")
                window.update()
                myCrawler = crawler.Crawler()
                myCrawler.startCrawler(job_get, country_get, level_get, int(amount_get))
                self.write_log("Finished crawling",self.success_tag)
            except Exception as e:
                print(e)
                self.write_log("Error when crawling. Please try again.", self.error_tag)

    def pandas_GUI(self, df =''):
        '''
            Opens the PandasGUI with the dataframe provided. If called with no parameters, open PandasGUI without a dataframe
            Parameters:
                df: pandas.DataFrame (optional) => The pandas DataFrame to be displayed
            Returns:
                None
        '''
        self.write_log("Opening Pandas Excel File Reader")
        window.update()
        show(df)

    def Open_git_Url(self):
        '''
            Opens the github website in a browser
            Parameters:
                None
            Returns:
                None
        '''
        self.write_log("Opening GitHub page in browser....")
        webbrowser.open_new("https://github.com/rawsashimi1604/JobExtract")

if __name__ == "__main__":
    window = tk.Tk()
    window.title("Job Extract")
    window.configure(background='#ADD8E6', pady = "20", padx ="10", height= 900, width=800)
    jobExtract_logo = PhotoImage(file="../../images/jobExtractLogowindow.png")
    jobExtract_logo_resized_window = jobExtract_logo.subsample(10,10)
    window.iconphoto(False, jobExtract_logo)
    myGUI = GUI(window)
    myGUI.startGUI()