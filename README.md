# LinkedIn Data Analysis on Job Descriptions

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
- Activate virtualenv, then install all required modules on your local machine.

```
    virtualenv venv
    source ./venv/Scripts/activate
    pip install -r requirements.txt
```

- From there you should be good to go to start coding!
- After coding finish, deactivate virtualenv

```
    deactivate
```

## Timeline

- Aim to complete by: **10 Oct**
- Components:
  - **Data Crawling** - 27 Sept
    - Selenium
  - **Data Cleaning** - 6 Oct
    - Text Mining
    - TextBlob (Detecting English Job Descriptions)
    - NLTK
    - spaCy
    - Gensim
  - **Data Analysis** - 10 Oct
    - Seaborn
    - Matplotlib

## Structure

Files are split into 2 folders, src and venv. **DO NOT ADD OR REMOVE FILES IN THE VENV FOLDER!**
For src:

```
    src
      |_ controller (all logic related code)
      |_ models (data)
      |_ views (analysis)
      |_ misc (misc code)
```

## Useful Resources

- [Learn Git In 15 Minutes](https://www.youtube.com/watch?v=USjZcfj8yxE&ab_channel=ColtSteele)
- [Python OOP Tutorial 1: Classes and Instances](https://www.youtube.com/watch?v=ZDa-Z5JzLYM&t=5s&ab_channel=CoreySchafer) _- For learning Python Object Oriented Programming_
