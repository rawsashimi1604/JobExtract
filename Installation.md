# Installation Guide

## ICT 1002 Python Project

### Members: Xue Wang, Jon, Serene, Olivia, Gavin

This is our project for ICT 1002, where we were tasked to scrape data from LinkedIn and conduct job sentiment analysis from there.

## Installation

- Firstly, download the Google Chrome web driver [here](https://chromedriver.chromium.org/downloads), make sure that you installed the correct version for your browser!
- Put ChromeDriver into Environment PATH Variable.
- After that, check whether pip is installed on your computer, type this into your terminal

```
    pip
```

- Install virtualenv module using pip.

```
    pip install virtualenv
```

- Then, [install Git](https://git-scm.com/download/win) on your computer and pull the repo into your local machine.
- Activate virtualenv, then install all required modules on your local machine. Use command prompt instead of Windows PowerShell!

```
    virtualenv venv
    cd ./venv/Scripts
    activate
    pip install -r requirements.txt
```

- Pull from this repository using `git`, then change working branch to production branch

```
  git clone https://github.com/rawsashimi1604/1002_LinkedIn.git
  git branch -f production origin/production
  git checkout production
```

- From there you should be good to go to start coding!

- To add to the codebase use Git! `git add .` adds all changes, `git status` checks status of Git, `git commit -m ...` adds a message to your commit for better referencing, `git push origin production` pushes your code to our production branch!

```
  git add .
  git status
  git commit -m "<enter your message here>"
  git push origin production
```

- To pull from existing codebase (get our latest updates), this will pull anything from master into your current production branch.

```
  git pull
  git merge origin/production
```

- To install compelte NLTK Library required for data cleaning, run `nltk.download()`.

## Timeline

- **Completed!!!!**
- Components:
  - ~~**Data Crawling** - 27 Sept~~
    - ~~Selenium~~
  - ~~**Data Cleaning** - 6 Oct~~
    - ~~Lang Detect~~
    - ~~NLTK~~
  - ~~**Data Analysis** - 14 Oct~~
    - ~~Seaborn~~
    - ~~Matplotlib~~
  - ~~**GUI** - 14 Oct~~

## Structure

Files are split into 3 folders, src. images and venv. **DO NOT ADD OR REMOVE FILES IN THE VENV FOLDER!** Venv is installed by the user.

```
    venv Folder (activate when coding)
      |_ ...
    images Folder (images)
      |_ ...
    src Folder
      |_ controller Folder (all logic related code)
          |_ __init__.py
          |_ augmentor.py
          |_ cleaner.py
          |_ counter.py
          |_ crawler.py
          |_ merger.py
          |_ processor.py
          |_ models Folder (data objects)
              |_ __init__.py
              |_ jobs.py
              |_ keywords.py
              |_ keywordsLook.py
      |_ data Folder
          |_ augmentedData Folder
              |_ (augmented data files...)
          |_ mergedData Folder
              |_ (merged data files...)
          |_ cleanedData Folder
              |_ (cleaned data files...)
          |_ rawData Folder
              |_ (raw data files...)
          |_ keywords Folder
              |_ (keywords data files...)
      |_ views Folder (analysis and GUI)
          |_ __init__.py
          |_ graphicUI.py
          |_ analysisPlots Folder
              |_ (plots....)
          |_ analysisWordCloud Folder
              |_ word_cloud.py
      |_ misc Folder (misc code, installer)
    README.md
    Installation.md
    Analysis.md
    requirements.txt (used to install modules in venv)
```

## Useful Resources

- [Learn Git In 15 Minutes](https://www.youtube.com/watch?v=USjZcfj8yxE&ab_channel=ColtSteele)
- [Python OOP Tutorial 1: Classes and Instances](https://www.youtube.com/watch?v=ZDa-Z5JzLYM&t=5s&ab_channel=CoreySchafer) _- For learning Python Object Oriented Programming_
