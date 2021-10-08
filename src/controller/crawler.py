from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.remote.webelement import WebElement
import time
from datetime import datetime
from pathlib import Path
import csv
import sys
from random import uniform


class Crawler:
    def __init__(self):
        '''
            Initialize Crawler Class.
            Parameters:
                None
            Returns:
                None
        '''
        # Measure time
        self.start = time.time()

        self.driver = webdriver.Chrome()
        self.driver.get("https://sg.linkedin.com/jobs")
        self.driver.maximize_window()

        self.positionLevel = "All"
        self.location = "Singapore"
        self.jobTitle = "Sales"

        self.crawlCount = 0

    @staticmethod
    def buffer(minseconds: float, maxseconds: float):
        '''
            Instructs Crawler sleep for x seconds
            Parameters:
                "seconds" : int => Amount in seconds to sleep.
            Returns:
                None
        '''
        time.sleep(uniform(minseconds, maxseconds))

    @staticmethod
    def dateTime():
        '''
            Returns today's date and time
            Parameters:
                None
            Returns:
                None
        '''
        now = datetime.now()
        datetime_string = now.strftime("%Y_%m_%d_%H_%M")

        return datetime_string

    def getFileName(self):
        return rf"../data/rawData/{self.location}/{self.positionLevel}/{self.dateTime()}_{self.jobTitle}_dataFile.csv"

    def makeFileDirectory(self):
        path = Path(f"../data/rawData/{self.location}/{self.positionLevel}/")
        path.mkdir(parents=True, exist_ok=True)

    def navigate(self, location: str):
        '''
            Instructs crawler to Navigate to page.
            Parameters:
                "location" : str => Place to navigate
            Returns:
                None
        '''
        pass

    def moveToNextJob(self):
        '''
            Instructs crawler to move browser position to next job
            Parameters:
                None
            Returns:
                None
        '''
        body = self.driver.find_element_by_css_selector("body")

        # Press the Down Button 4 times
        for i in range(4):
            body.send_keys(Keys.DOWN)

        self.buffer(0.3, 0.5)

    def moveErrorJob(self, previousSibling: WebElement, currentSibling: WebElement):
        '''
            Instructs crawler to move browser position back to previous job description, click it, then go back to current job description.
            Parameters:
                previousSibilng: WebElement => previous job description
                currentSibiling: WebElement => current job description
            Returns:
                None
        '''
        body = self.driver.find_element_by_css_selector("body")

        self.buffer(0.3, 0.7)
        # Press the Up button 4 times
        for i in range(4):
            body.send_keys(Keys.UP)

        # Click the previous sibling element
        previousSibling.click()

        self.buffer(0.3, 0.7)
        # Press the Down button 4 times
        for i in range(4):
            body.send_keys(Keys.DOWN)

        # Click the current sibling element
        currentSibling.click()
        self.buffer(0.3, 0.7)

    def searchJobs(self, jobTitle: str, location: str):
        '''
            Instructs crawler to search jobs
            Parameters:
                "jobTitle" : str => Job Title Name
                "location" : str => Location of jobs
            Returns:
                None
        '''

        self.buffer(1.5, 2.5)

        # Finds the <body> tag
        body = self.driver.find_element_by_css_selector("body")
        if self.driver.current_url == "https://sg.linkedin.com/jobs":
            # Find the search companies <input> tag
            searchCompaniesInput = self.driver.find_element_by_css_selector(
                "input[aria-label='Search job titles or companies']")
            searchCompaniesInput.send_keys(jobTitle)

            # Find the location <input> tag
            locationInput = self.driver.find_element_by_css_selector(
                "input[aria-label='Location']")
            locationInput.clear()
            locationInput.send_keys(location)

            # Press DOWN and ENTER Key
            self.buffer(0.5, 1.5)
            locationInput.send_keys(Keys.DOWN)
            self.buffer(0.5, 1.5)
            locationInput.send_keys(Keys.ENTER)

        self.jobTitle = jobTitle
        self.location = location

    def selectPositionLevel(self, position: str):
        '''
            Instructs crawler to select position level
            Parameters:
                "position" : str => Job Position Level
                Available Parameters:
                    "Internship",
                    "Entry",
                    "Associate",
                    "Mid-Senior",
                    "Director"
            Returns:
                None
        '''
        positionArray = [
            "All",
            "Internship",
            "Entry",
            "Associate",
            "Mid-Senior",
            "Director"
        ]

        if position != "All":
            # Find the Experience Level <button> tag
            self.buffer(1.5, 2.5)
            expLevelButton = self.driver.find_element_by_css_selector(
                "button[aria-label='Experience Level filter. Clicking this button displays all Experience Level filter options.']")
            expLevelButton.click()

            # Find the Position Level <label>, and their parent <div>
            parentDiv = expLevelButton.find_element_by_xpath('..')
            fieldSetDiv = parentDiv.find_element_by_css_selector(
                "div > fieldset > div")
            positionDivs = fieldSetDiv.find_elements_by_css_selector("div")

            # Click on the Job Position <label>
            for pos in positionDivs:
                positionLabel = pos.find_element_by_css_selector(
                    "label")
                positionLabelText = positionLabel.text.split(" ")[0]
                # positionCheckBox = pos.find_element_by_css_selector("input")
                if position == positionLabelText:
                    self.buffer(0.3, 0.7)
                    positionLabel.click()
                    break

            # Click on the Done <button>
            doneButton = parentDiv.find_element_by_css_selector(
                "div > button[aria-label='Apply filters']")
            self.buffer(0.3, 0.7)
            doneButton.click()

            # Set global instance var
            self.positionLevel = position

    def getJobInfo(self, jobCount: int):
        '''
            Instructs crawler to scrape job description data
            Parameters:
                jobCount: int => Number of jobs descriptions to scrape
            Returns:
                None
        '''

        # Create File Directory, Create CSV file
        self.makeFileDirectory()
        fileName = self.getFileName()

        # Creates CSV File for storing data
        with open(fileName, "w", encoding="utf-8", newline='') as csvFile:

            # Initialize CSV DictWriter
            csvColumns = ['jobTitle', 'companyName', 'location', 'datePosted', 'appStatus',
                          'description', 'seniorityLevel', 'employmentType', 'jobFunction', 'industries']
            writer = csv.DictWriter(csvFile, fieldnames=csvColumns)
            writer.writeheader()

            # Finds the <body> tag and <ul> tag for scraping.
            body = self.driver.find_element_by_css_selector("body")
            unorderedList = self.driver.find_element_by_css_selector(
                "ul[class='jobs-search__results-list']")

            # Moves the browser to location of first <li> tag
            for i in range(6):
                body.send_keys(Keys.DOWN)

            # Finds the first <li> tag
            currentLi = unorderedList.find_element_by_css_selector("li")
            currentLi.click()
            self.buffer(1.5, 2.5)

            # SCRAPE INFO
            for i in range(jobCount):
                try:
                    # Moves browser in position for scraping
                    self.moveToNextJob()

                    # Finds the previous <li> tag
                    prevLi = currentLi

                    # Finds the next <li> tag
                    currentLi = currentLi.find_element_by_xpath(
                        "following-sibling::*")

                    currentLi.click()
                    self.buffer(0.5, 1.5)
                    currentLi.click()
                    self.buffer(0.5, 1.5)

                    # Check whether <li> was clicked and data is showing
                    for _ in range(5):
                        # Attempt to fix job description not showing bug
                        if not self.tryToFindData():
                            self.moveErrorJob(prevLi, currentLi)

                        else:
                            break

                    # Get data from LinkedIn
                    data = self.getJobData()
                    if data:
                        print(f"{i} : Successfully got {data} \n\n")

                        # Append data to CSV File
                        writer.writerow(data)
                        self.crawlCount += 1
                    else:
                        continue

                except (ElementNotInteractableException, NoSuchElementException):
                    pass

                # Finds the see more <button>, then clicks on it. Allows crawler to scrape more job descriptions.
                try:
                    seeMoreButton = unorderedList.find_element_by_xpath(
                        "..").find_element_by_css_selector("button[aria-label='Load more results']")
                    seeMoreButton.click()
                except ElementNotInteractableException:
                    pass

            # Close CSV File after writing to prevent memory leakage
            csvFile.close()

    def getJobData(self):
        '''
            Instructs crawler to scrape job description data
            Parameters:
                None
            Returns:
                dictionary => dictionary keys: dataType, dictionary values: dataValues
        '''
        # Find the Show More <button>, If it exists, click it
        try:
            showMoreButton = self.driver.find_element_by_css_selector(
                "button[aria-label= 'Show more, visually expands previously read content above this button']")
            showMoreButton.click()
            self.buffer(1.5, 2.5)
        except (NoSuchElementException, ElementNotInteractableException):
            pass

        # Find the content <div> for job description information
        try:
            contentDiv = self.driver.find_element_by_css_selector(
                "div[class='details-pane__content details-pane__content--show']")

        except NoSuchElementException:
            return

        jobTitle = self.scrapeJobTitle(contentDiv)
        companyName = self.scrapeCompanyName(contentDiv)
        location = self.scrapeLocation(contentDiv)
        datePosted = self.scrapeDatePosted(contentDiv)
        appStatus = self.scrapeApplicantsStatus(contentDiv)
        description = self.scrapeDescription(contentDiv)

        seniorityLevel = self.scrapeSeniorityLevel(contentDiv)
        employmentType = self.scrapeEmploymentType(contentDiv)
        jobFunction = self.scrapeJobFunction(contentDiv)
        industries = self.scrapeIndustries(contentDiv)

        dataDictionary = {
            "jobTitle": jobTitle,
            "companyName": companyName,
            "location": location,
            "datePosted": datePosted,
            "appStatus": appStatus,
            "description": description,
            "seniorityLevel": seniorityLevel,
            "employmentType": employmentType,
            "jobFunction": jobFunction,
            "industries": industries,
        }

        return dataDictionary

    def tryToFindData(self):
        '''
            Instructs crawler to try to find job description data
            Parameters:
                None
            Returns:
                bool => True if data is found, False if data is not found
        '''
        # Try to find Job Title <h2>
        try:
            self.driver.implicitly_wait(0.5)
            h2 = self.driver.find_element_by_css_selector(
                "h2[class='top-card-layout__title topcard__title']").text

            return not(h2 == "")

        # If unable to find
        except StaleElementReferenceException:
            return False

    def scrapeJobTitle(self, currentDiv: WebElement):
        try:
            jobTitle = currentDiv.find_element_by_css_selector(
                "h2[class='top-card-layout__title topcard__title']").text
            return jobTitle.strip().replace("\n", " ")

        except NoSuchElementException:
            return ""

    def scrapeCompanyName(self, currentDiv: WebElement):
        try:
            companyName = currentDiv.find_element_by_css_selector(
                "a[data-tracking-control-name='public_jobs_topcard-org-name']").text
            return companyName.strip().replace("\n", " ")

        except NoSuchElementException:
            return ""

    def scrapeLocation(self, currentDiv: WebElement):
        try:
            location = currentDiv.find_element_by_css_selector(
                "span[class='topcard__flavor topcard__flavor--bullet']").text
            return location.strip().replace("\n", " ")

        except NoSuchElementException:
            return ""

    def scrapeDatePosted(self, currentDiv: WebElement):
        try:
            datePosted = currentDiv.find_element_by_css_selector(
                "span[class='posted-time-ago__text topcard__flavor--metadata']").text
            datePosted = datePosted.strip().replace("\n", " ")

            if not datePosted:
                datePosted = currentDiv.find_element_by_css_selector(
                    "span[class='posted-time-ago__text posted-time-ago__text--new topcard__flavor--metadata']").text
                return datePosted.strip().replace("\n", " ")

            return datePosted

        except NoSuchElementException:
            return ""

    def scrapeApplicantsStatus(self, currentDiv: WebElement):
        try:
            applicantsStatus = currentDiv.find_element_by_css_selector(
                "figcaption[class='num-applicants__caption']").text
            applicantsStatus = applicantsStatus.strip().replace("\n", " ")

            return applicantsStatus

        except NoSuchElementException:
            try:
                applicantsStatus = self.driver.find_element_by_css_selector(
                    "span[class='num-applicants__caption topcard__flavor--metadata topcard__flavor--bullet']").get_attribute('innerHTML')
                return applicantsStatus.strip().replace("\n", " ")
            except NoSuchElementException:
                return ""

    def scrapeDescription(self, currentDiv: WebElement):
        try:
            description = currentDiv.find_element_by_css_selector(
                "div[class='show-more-less-html__markup']").text
            return description.strip().replace("\n", " ")

        except NoSuchElementException:
            return ""

    def scrapeSeniorityLevel(self, currentDiv: WebElement):
        try:
            unorderedList = currentDiv.find_element_by_css_selector(
                "ul[class='description__job-criteria-list']").find_elements_by_css_selector("li")
            for element in unorderedList:
                label = element.find_element_by_css_selector("h3")
                data = element.find_element_by_css_selector("span")
                if "Seniority level" in label.text:
                    return data.text.strip().replace("\n", " ")

        except NoSuchElementException:
            return ""

    def scrapeEmploymentType(self, currentDiv: WebElement):
        try:
            unorderedList = currentDiv.find_element_by_css_selector(
                "ul[class='description__job-criteria-list']").find_elements_by_css_selector("li")
            for element in unorderedList:
                label = element.find_element_by_css_selector("h3")
                data = element.find_element_by_css_selector("span")
                if "Employment type" in label.text:
                    return data.text.strip().replace("\n", " ")

        except NoSuchElementException:
            return ""

    def scrapeJobFunction(self, currentDiv: WebElement):
        try:
            unorderedList = currentDiv.find_element_by_css_selector(
                "ul[class='description__job-criteria-list']").find_elements_by_css_selector("li")
            for element in unorderedList:
                label = element.find_element_by_css_selector("h3")
                data = element.find_element_by_css_selector("span")
                if "Job function" in label.text:
                    return data.text.strip().replace("\n", " ")

        except NoSuchElementException:
            return ""

    def scrapeIndustries(self, currentDiv: WebElement):
        try:
            unorderedList = currentDiv.find_element_by_css_selector(
                "ul[class='description__job-criteria-list']").find_elements_by_css_selector("li")
            for element in unorderedList:
                label = element.find_element_by_css_selector("h3")
                data = element.find_element_by_css_selector("span")
                if "Industries" in label.text:
                    return data.text.strip().replace("\n", " ")

        except NoSuchElementException:
            return ""

    def exitCrawler(self):
        '''
            Instructs crawler to exit and close browser.
            Parameters:
                None
            Returns:
                None
        '''
        self.buffer(1.5, 2.5)
        self.driver.close()
        print(f'''
*****************************************************************************************        
Crawling has ended, browser has been closed.

*****************************************************************************************
Statistics :
*****************************************************************************************

### Time taken for code : {round((time.time() - self.start) / 60, 2)} minutes
### Total data crawled : {self.crawlCount}
### File directory saved to : {self.getFileName()}

Thank you for using the crawler.
*****************************************************************************************   
        ''')


if __name__ == "__main__":
    myCrawler = Crawler()
    # First arg => Job
    # Second arg => Location
    myCrawler.searchJobs("Sales", "Russia")

    # First arg => Position Levels
    # Avail =>  [
    #         "All",
    #         "Internship",
    #         "Entry",
    #         "Associate",
    #         "Mid-Senior",
    #         "Director"
    #     ]
    myCrawler.selectPositionLevel("All")
    myCrawler.getJobInfo(5)
    myCrawler.exitCrawler()
