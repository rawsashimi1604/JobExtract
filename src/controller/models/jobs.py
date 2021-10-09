class JobsModel:
    def __init__(self, jobTitle, companyName, location, datePosted, appStatus, description, seniorityLevel, employmentType, jobFunction, industries):
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

    def __repr__(self):
        return f"<JobsModel object => jobTitle: {self.jobTitle}, companyName: {self.companyName}, location: {self.location}, datePosted: {self.datePosted}, appStatus: {self.appStatus}, description: {self.description}, seniorityLevel: {self.seniorityLevel}, employmentType: {self.employmentType}, jobFunction: {self.jobFunction}, industries: {self.industries}>\n"

    def __str__(self):
        return f"JobsModel attributes: <JobsModel jobTitle: {self.jobTitle}, companyName: {self.companyName}, location: {self.location}, datePosted: {self.datePosted}, appStatus: {self.appStatus}, description: {self.description}, seniorityLevel: {self.seniorityLevel}, employmentType: {self.employmentType}, jobFunction: {self.jobFunction}, industries: {self.industries}>\n"

    def updateValues(self):
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


def printWorld():
    print("Hello world")
