import tkinter as tk
from os import getcwd
import sys
from tkinter.constants import WORD
sys.path.append('../controller')
import cleaner

class GUI:
    def __init__(self):
        self.filename = ""
        self.window = tk.Tk()

    def startGUI(self):
        window = self.window
        window.title("LinkedIn Data Cleaner")
        window.configure(background='white', pady = "20", padx ="10")
        greeting = tk.Label(
            text='Welcome to LinkedIn cleaner bot!',
            background= 'white',
            width=100,
            height=10
        )
        clean_button = tk.Button(
            text='Clean data file',
            background = "#cfcfcf",
            command= self.chooseDirectory,
        )
        # status_text = tk.Text(
        #     window, 
        #     width=80, 
        #     height=30,
        #     wrap=WORD
        # )
        # status_text.pack()
        greeting.pack()
        clean_button.pack(pady=10)
        window.mainloop()

    def chooseDirectory(self):
        cwd = getcwd()
        self.filename = tk.filedialog.askopenfile(initialdir=cwd, title="Select Data File", filetypes=(("CSV files","*.csv"),("all files","*.*"))).name
        self.startCleaner()

    def startCleaner(self):
        myCleaner = cleaner.Cleaner()
        
        try:
            myCleaner.startCleaner(self.filename)
            cleaning_text = 'Successfully cleaned {}'.format(self.filename)
            cleaning_status = tk.Label(
                text=cleaning_text,
                fg='green'
            )
            cleaning_status.pack()
            # status_text.insert('1.0', cleaning_text)
        except KeyError:
            error_status = tk.Label(
                text= 'Error when cleaning file {}'.format(self.filename),
                fg = 'red'
            )
            error_status.pack()

if __name__ == "__main__":
    myGUI = GUI()
    myGUI.startGUI()