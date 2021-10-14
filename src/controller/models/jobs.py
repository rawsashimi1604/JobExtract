from __future__ import annotations

"""
    Jobs Module. Contains JobsModel Object, utility object used to help with storage of jobs in CSV.
"""

class JobsModel:
    '''
        JobsModel Object, utility object used to help with storage of jobs in CSV.

        Class Attributes:
            jobTitle : str => Job Title
            companyName : str => Company Name
            location : str => Location
            datePosted : str => Date Posted
            appStatus : str => Applicants Status
            description : str => Job Description
            seniorityLevel : str => Seniority Level
            employmentType : str => Employement Type
            jobFunction : str => Job Function
            industries : str => Job Industries
    '''
    def __init__(self, jobTitle: str, companyName: str, location: str, datePosted: str, appStatus: str, description: str, seniorityLevel: str, employmentType: str, jobFunction: str, industries: str) -> JobsModel:
        '''
            Constructor for JobsModel Class.
            Parameters:
                jobTitle : str => Job Title
                companyName : str => Company Name
                location : str => Location
                datePosted : str => Date Posted
                appStatus : str => Applicants Status
                description : str => Job Description
                seniorityLevel : str => Seniority Level
                employmentType : str => Employement Type
                jobFunction : str => Job Function
                industries : str => Job Industries
            Returns:
                JobsModel => Constructs JobsModel Class
        '''
        self.jobTitle = jobTitle
        self.companyName = companyName
        self.location = location
        self.datePosted = datePosted
        self.appStatus = appStatus
        self.description = description
        self.seniorityLevel = seniorityLevel
        self.employmentType = employmentType
        self.jobFunction = jobFunction
        self.industries = industries

        self.parameters = [
            "jobTitle",
            "companyName",
            "location",
            "datePosted",
            "appStatus",
            "description",
            "seniorityLevel",
            "employmentType",
            "jobFunction",
            "industries"
        ]

        self.objectValues = [
            self.jobTitle,
            self.companyName,
            self.location,
            self.datePosted,
            self.appStatus,
            self.description,
            self.seniorityLevel,
            self.employmentType,
            self.jobFunction,
            self.industries
        ]

    def __repr__(self) -> str:
        '''
            Print for Object
            Parameters:
                None
            Returns:
                str => Print message
        '''
        return f"<JobsModel object => jobTitle: {self.jobTitle}, companyName: {self.companyName}, location: {self.location}, datePosted: {self.datePosted}, appStatus: {self.appStatus}, description: {self.description}, seniorityLevel: {self.seniorityLevel}, employmentType: {self.employmentType}, jobFunction: {self.jobFunction}, industries: {self.industries}>\n"

    def __str__(self) -> str:
        '''
            Print for Object
            Parameters:
                None
            Returns:
                str => Print message
        '''
        return f"JobsModel attributes: <JobsModel jobTitle: {self.jobTitle}, companyName: {self.companyName}, location: {self.location}, datePosted: {self.datePosted}, appStatus: {self.appStatus}, description: {self.description}, seniorityLevel: {self.seniorityLevel}, employmentType: {self.employmentType}, jobFunction: {self.jobFunction}, industries: {self.industries}>\n"

    def updateValues(self) -> None:
        '''
            Updates object values
            Parameters:
                None
            Returns:
                None
        '''
        self.objectValues = [
            self.jobTitle,
            self.companyName,
            self.location,
            self.datePosted,
            self.appStatus,
            self.description,
            self.seniorityLevel,
            self.employmentType,
            self.jobFunction,
            self.industries
        ]
