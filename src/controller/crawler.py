from selenium import webdriver
import selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementNotInteractableException
import time

from selenium.webdriver.ie.options import ElementScrollBehavior

#testest
class Crawler:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://sg.linkedin.com/jobs")
        self.driver.maximize_window()

    @staticmethod
    def buffer(seconds: int):
        '''
            Instructs Crawler sleep for x seconds
            Parameters:
                "seconds" : int => Amount in seconds to sleep.
            Returns:
                None
        '''
        time.sleep(seconds)

    def navigate(self, location: str):
        '''
            Instructs crawler to Navigate to page.
            Parameters:
                "location" : str => Place to navigate
            Returns:
                None
        '''
        pass

    def searchJobs(self, jobTitle: str, location: str):
        '''
            Instructs crawler to search jobs
            Parameters:
                "jobTitle" : str => Job Title Name
                "location" : str => Location of jobs
            Returns:
                None
        '''

        self.buffer(2)

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
            self.buffer(1)
            locationInput.send_keys(Keys.DOWN)
            self.buffer(1)
            locationInput.send_keys(Keys.ENTER)

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
            "Internship",
            "Entry",
            "Associate",
            "Mid-Senior",
            "Director"
        ]

        # Find the Experience Level <button> tag
        self.buffer(2)
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
                self.buffer(0.5)
                positionLabel.click()
                print("clicked")
                break

        # Click on the Done <button>
        doneButton = parentDiv.find_element_by_css_selector(
            "div > button[aria-label='Apply filters']")
        self.buffer(0.5)
        doneButton.click()

    def getJobInfo(self):
        '''
            Instructs crawler to scrape job description data
            Parameters:
                None
            Returns:
                None
        '''
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
        self.buffer(2)

        # SCRAPE INFO
        for i in range(1000):
            # Moves browser in position for scraping
            self.moveToNextJob()

            # Finds the next <li> tag
            currentLi = currentLi.find_element_by_xpath(
                "following-sibling::*")
            currentLi.click()
            self.buffer(1)
            currentLi.click()
            self.buffer(1)

            # Finds the see more <button>, then clicks on it. Allows crawler to scrape more job descriptions.
            try:
                seeMoreButton = unorderedList.find_element_by_xpath(
                    "..").find_element_by_css_selector("button[aria-label='Load more results']")
                seeMoreButton.click()
            except ElementNotInteractableException:
                pass

    def selectJob(self):
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

    def exitCrawler(self):
        '''
            Instructs crawler to exit and close browser.
            Parameters:
                None
            Returns:
                None
        '''
        self.buffer(2)
        self.driver.close()


myCrawler = Crawler()
myCrawler.searchJobs("Sales", "Singapore")
myCrawler.getJobInfo()
