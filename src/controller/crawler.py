from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time


class Crawler:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://sg.linkedin.com/jobs")
        self.driver.maximize_window()

    @staticmethod
    def buffer(seconds: int):
        '''
            Makes Crawler sleep for x seconds
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
        if self.driver.current_url == "https://sg.linkedin.com/jobs":
            # Find the search companies <input> tag
            searchCompaniesInput = self.driver.find_element_by_css_selector(
                "input[aria-label='Search job titles or companies']")
            searchCompaniesInput.send_keys(jobTitle)
            self.buffer(0.2)

            # Find the location <input> tag
            locationInput = self.driver.find_element_by_css_selector(
                "input[aria-label='Location']")
            locationInput.clear()
            locationInput.send_keys(location)
            self.buffer(0.2)

            # Find the Search Jobs <button> tag
            searchButton = self.driver.find_element_by_css_selector(
                "button[data-searchbar-type='JOBS']")
            searchButton.click()

    def selectPositionLevel(self, position: str):
        '''
            Instructs crawler to select position level
            Parameters:
                "position" : str => Job Position Level
                Available Parameters:
                    "Internship",
                    "Entry level",
                    "Associate",
                    "Mid-Senior level",
                    "Director"
            Returns:
                None
        '''
        positionArray = [
            "Internship",
            "Entry level",
            "Associate",
            "Mid-Senior level",
            "Director"
        ]

        # Find the Experience Level <button> tag
        self.buffer(2)
        expLevelButton = self.driver.find_element_by_css_selector(
            "button[aria-label='Experience Level filter. Clicking this button displays all Experience Level filter options.']")
        expLevelButton.click()

        # Find the Position Level Checkboxes
        parentDiv = expLevelButton.find_element_by_xpath('..')
        fieldSetDiv = parentDiv.find_element_by_css_selector(
            "div > fieldset > div")
        positionDivs = fieldSetDiv.find_elements_by_css_selector("div")

        # Click on the Job Position Label
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

        # Click on the Done Button
        doneButton = parentDiv.find_element_by_css_selector(
            "div > button[aria-label='Apply filters']")
        self.buffer(0.5)
        doneButton.click()

    def exitCrawler(self):
        self.driver.close()


myCrawler = Crawler()
myCrawler.searchJobs("Software Engineer", "Singapore")
myCrawler.selectPositionLevel("Internship")
