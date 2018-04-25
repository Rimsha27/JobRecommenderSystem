import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from pymongo import MongoClient
from accounts import models
from . import recommendationAlgos

jobs = []

class Jobs(object):
    # Note that we're taking an argument besides self, here.
    def __init__(self, id=0, jobTitle="", jobCompany="", jobLocation="", jobSalary="", jobSummary="", jobLink=""):
        self.id = id
        self.jobTitle = jobTitle
        self.jobCompany = jobCompany
        self.jobLocation = jobLocation
        self.jobSalary = jobSalary
        self.jobSummary = jobSummary
        self.jobLink = jobLink


def jobsviewing(request):
    return render(request, 'jobs.html')

# This Function Stores Implicit Feedback
def displayingJobDetail(request):
    if request.method == "POST":
        global jobs
        connection = MongoClient(port=27017)

        implicitFbDB = connection.ImplicitFeedback

        jobsDB = connection.Jobs
        jobDetailsCollection = jobsDB.jobsDetail

        storedJobs = connection.JobDatabase
        storedJobsCollection= storedJobs.Jobs

        # Here I will first get the Job id from the Hidden Text Box
        jobId = [key for key in request.POST if key.startswith("jobId")]
        jobType = [key for key in request.POST if key.startswith("jobType")]

        # Getting the username
        username = request.user.username

        # Now retrieving the Django object corresponding to it from the Sqlite3 Database
        UserRecord = models.signupModel.objects.filter(email=username)

        # Getting the Job
        jobId = jobId[0].split("+")
        jobId = int(jobId[1])
        jobType = jobType[0].split("+")
        jobType = jobType[1]
        print(jobType)
        jobToBeStored = ""

        #there is no job in Jobs Database
        if jobDetailsCollection.count() == 0:
            print("Job Rated Database is empty")
            if jobType == "False":
                print("The job is the searched job")
                jobToBeStored = jobs[jobId - 1]
            else:
                print("The job is the stored job")
                jobsData = storedJobsCollection.find_one({"ID": jobId})
                try:
                    salary = jobsData.Salary
                except:
                    salary = ""
                try:
                    applyLink = jobsData.ApplyLink
                except:
                    applyLink = ""
                jobToBeStored = Jobs(jobsData['ID'], jobsData['Title'], jobsData['Company'], jobsData['Location'],
                                     salary, jobsData['Summary'], applyLink)
            jobId = 15001
            Job = {
                'userassignedId': jobId,
                'JobTitle': jobToBeStored.jobTitle,
                'JobCompany': jobToBeStored.jobCompany,
                'JobLocation': jobToBeStored.jobLocation,
                'JobSalary': jobToBeStored.jobSalary,
                'JobSummary': jobToBeStored.jobSummary,
                'JobApplyLink': jobToBeStored.jobLink,
            }
            result = jobDetailsCollection.insert_one(Job)
            print("inserted")

        #Jobs Database is not empty
        else:
            # check if the job already exists or not
            print("Job collection is not empty")
            print(jobId)
            jobsData = jobDetailsCollection.find_one({"userassignedId": jobId})
            print(jobsData)

            #If does not exists, retrieve the number of jobs and assign count+1 as jobId
            if jobsData is None:
                if jobType == "False":
                    print("The job is the searched job")
                    jobToBeStored = jobs[jobId - 1]
                    jobsData = jobDetailsCollection.find_one({"JobTitle": jobToBeStored.jobTitle})

                    #This covers the scenario when a user has clicked a searched job and then he again searches and the same job appers, the jobId will be local so we are searching on job title
                    if jobsData is not None:
                        jobId = jobsData['userassignedId']
                    else:
                        no_of_documents = jobDetailsCollection.count();
                        jobId = 15000 + no_of_documents + 1
                        Job = {
                            'userassignedId': jobId,
                            'JobTitle': jobToBeStored.jobTitle,
                            'JobCompany': jobToBeStored.jobCompany,
                            'JobLocation': jobToBeStored.jobLocation,
                            'JobSalary': jobToBeStored.jobSalary,
                            'JobSummary': jobToBeStored.jobSummary,
                            'JobApplyLink': jobToBeStored.jobLink,
                        }
                        result = jobDetailsCollection.insert_one(Job)
                        print("inserted")
                else:
                    print("The job is the stored job")
                    jobsData = storedJobsCollection.find_one({"ID": jobId})
                    try:
                        salary = jobsData.Salary
                    except:
                        salary = ""
                    try:
                        applyLink = jobsData.ApplyLink
                    except:
                        applyLink = ""
                    jobToBeStored = Jobs(jobsData['ID'], jobsData['Title'], jobsData['Company'], jobsData['Location'],
                                         salary,
                                         jobsData['Summary'], applyLink)
                    jobsData = jobDetailsCollection.find_one({"JobTitle": jobToBeStored.jobTitle})

                    # This covers the scenario when a user has clicked a recommended job(from CBR) and then he again clicks, its id will be the one from storedJobs so we'll search based on jobTitle
                    if jobsData is not None:
                        jobId = jobsData['userassignedId']
                    else:
                        no_of_documents = jobDetailsCollection.count();
                        jobId = 15000 + no_of_documents + 1
                        Job = {
                            'userassignedId': jobId,
                            'JobTitle': jobToBeStored.jobTitle,
                            'JobCompany': jobToBeStored.jobCompany,
                            'JobLocation': jobToBeStored.jobLocation,
                            'JobSalary': jobToBeStored.jobSalary,
                            'JobSummary': jobToBeStored.jobSummary,
                            'JobApplyLink': jobToBeStored.jobLink,
                        }
                        result = jobDetailsCollection.insert_one(Job)
                        print("inserted")
            else:
                jobId = jobsData['userassignedId']
                jobToBeStored = Jobs(jobsData['userassignedId'], jobsData['JobTitle'], jobsData['JobCompany'], jobsData['JobLocation'],
                                     jobsData['JobSalary'], jobsData['JobSummary'], jobsData['JobApplyLink'])

        #If the user has rated the job before
        feed_back_of_user = implicitFbDB.reviews.find_one({"Userid": UserRecord[0].idformongo, "Jobid": jobId})
        #If he hadn't
        if feed_back_of_user is None:
            print("Nothing initially in the DB")
            implicit_feedback_count = 1
            Feedback = {
                'Userid': UserRecord[0].idformongo,
                'Jobid': jobId,
                'ImplicitRating': implicit_feedback_count
            }
            result = implicitFbDB.reviews.insert_one(Feedback)
        #f he had
        else:
            # This means that the User has already opened this job and gave implplicit rating
            # So increasing the previous count Would do the job
            # Incrementing the Job Implicit Rating
            implicitFbDB.reviews.update(
                {'Userid': UserRecord[0].idformongo, 'Jobid': jobId},
                {
                    "$inc": {"ImplicitRating": 1}
                }
            )
        return render(request, 'jobsDetail.html', {"jobsDetail": jobToBeStored, "isStoredJob": jobType})
    else:
        return render(request, 'Signinform.html')

def jobsretrieving(request):
    if request.method == "POST":
        global jobs
        jobs = []

        id_temp = ""
        jobTitle_temp = ""
        jobCompany_temp = ""
        jobLocation_temp = ""
        jobSalary_temp = ""
        jobSummary_temp = ""
        jobLink_temp = ""

        desc = "web"
        loc = ""
        j = 1
        start = 0

        while start is not 20:
            r = requests.get("https://www.indeed.com/jobs?q=" + request.POST['keyword'] + "&l=" + request.POST[
                'location'] + "&start=" + str(start),
                             proxies={"http": "http://61.233.25.166:80"})
            start += 10
            data = r.text
            soup = BeautifulSoup(data, 'lxml')
            soup = soup.findAll("a", {"class": "turnstileLink"})

            for link in soup:
                jobLink = link.get("href")
                if "clk" in jobLink:
                    jobRequest = requests.get("https://www.indeed.com" + jobLink,
                                              proxies={"http": "http://61.233.25.166:80"})
                    jobData = jobRequest.text
                    jobSoup = BeautifulSoup(jobData, 'lxml')

                    id_temp = j

                    print("JobID", id_temp)

                    jobTitle = jobSoup.find("b", {"class": "jobtitle"})
                    jobData = jobTitle.text

                    jobTitle_temp = jobTitle.text

                    print("JobTitle", jobTitle_temp)

                    jobCompany = jobSoup.find("span", {"class": "company"})

                    if jobCompany:
                        jobData = jobData + " " + jobCompany.text
                        jobCompany_temp = jobCompany.text

                        print(jobCompany_temp)

                    jobLocation = jobSoup.find("span", {"class": "location"})

                    if jobLocation:
                        jobData = jobData + " " + jobLocation.text
                        jobLocation_temp = jobLocation.text

                        print(jobLocation_temp)

                    jobSalary = jobSoup.find("span", {"class": "no-wrap"})
                    if jobSalary:
                        jobData = jobData + " " + jobSalary.text
                        jobSalary_temp = jobSalary.text

                        print(jobSummary_temp)

                    jobApplyLink = jobSoup.find("a", {"class": "view_job_link view-apply-button blue-button"})
                    if jobApplyLink:
                        jobApplyLink = "https://www.indeed.com" + jobApplyLink.get("href")
                        jobLink_temp = jobApplyLink
                        print(jobApplyLink)

                    jobSummary = jobSoup.find("span", {"class": "summary"})
                    if jobSummary:
                        jobData = jobData + " " + jobSummary.text
                        jobSummary_temp = jobSummary.text

                        # print(jobSummary_temp)

                    jobs.append(Jobs(id_temp, jobTitle_temp, jobCompany_temp, jobLocation_temp, jobSalary_temp,
                                     jobSummary_temp, jobLink_temp))
                    print(id_temp)
                    j += 1
        return render(request, 'jobs.html', {"jobList": jobs, "isStoredJob": False })
    else:
        return render(request, 'Signinform.html')

def saveExplicitRating(request):
    if request.method == "POST":
        global jobs
        connection = MongoClient(port=27017)
        explicitFbDB = connection.ExplicitFeedback
        jobsDB = connection.Jobs
        jobDetailsCollection = jobsDB.jobsDetail

        actual_star_number_and_job_number = request.POST.get('star')
        jobType = [key for key in request.POST if key.startswith("jobType")]
        jobType = jobType[0].split("+")
        jobType = jobType[1]


        # Getting the username
        username = request.user.username

        # Now retrieving the Django object corresponding to it from the Sqlite3 Database
        UserRecord = models.signupModel.objects.filter(email=username)

        # Getting the JobTitle
        Number = actual_star_number_and_job_number.split("+")
        print("Star Rating is", Number[1])
        print("Job id is ", Number[2])

        jobId = int(Number[2])

        jobsData = jobDetailsCollection.find_one({"userassignedId": jobId})
        print(jobsData)

        # If does not exists, retrieve the number of jobs and assign count+1 as jobId
        if jobsData is None:

            if jobType == "False":
                jobToBeStored = jobs[jobId - 1]
                jobTitle = jobToBeStored.jobTitle
                jobsData = jobDetailsCollection.find_one({"JobTitle": jobTitle})
                jobId = jobsData['userassignedId']
            else:
                storedJobs = connection.JobDatabase
                storedJobsCollection = storedJobs.Jobs

                jobsData = storedJobsCollection.find_one({"ID": jobId})
                jobTitle = jobsData['Title']
                jobsData = jobDetailsCollection.find_one({"JobTitle": jobTitle})
                jobId = jobsData['userassignedId']

        # If the user has rated the job before
        feed_back_of_user = explicitFbDB.reviews.find_one({"Userid": UserRecord[0].idformongo, "Jobid": jobId})

        # If he hadn't
        if feed_back_of_user is None:
            print("Nothing initially in the DB")
            Feedback = {
                'Userid': UserRecord[0].idformongo,
                'Jobid': jobId,
                'ExplicitRating': Number[1]
            }
            result = explicitFbDB.reviews.insert_one(Feedback)
        #If he had, update the rating
        else:
            explicitFbDB.reviews.update(
                {"Jobid": jobId, "Userid": UserRecord[0].idformongo},
                {"$set": {"ExplicitRating": Number[1]}}
            )
        return render(request, 'jobs.html', {"jobList": jobs, "isStoredJob": jobType})
    else:
        return render(request, 'Signinform.html')

def recommendjobs(request):
    if request.method == "POST":
        username = request.user.username
        UserRecord = models.signupModel.objects.filter(email=username)
        ID = UserRecord[0].idformongo
        recommendedJobIDsUsingContent = recommendationAlgos.contentBasedRecommendations(ID)
        recommendedJobIDsUsingALS = recommendationAlgos.ALSrecommendations(ID)
        print(recommendedJobIDsUsingContent)
        print(recommendedJobIDsUsingALS)
        connection = MongoClient(port=27017)

        db = connection.JobDatabase
        jobs = db.Jobs
        recommendedJobs = []
        i=0
        for jobId in recommendedJobIDsUsingContent:
            if i==3:
                break;
            job = jobs.find_one({"ID": jobId})
            print(job)
            try:
                salary = job['Salary']
            except:
                salary = ""
            try:
                applyLink = job['ApplyLink']
            except:
                applyLink = ""
            recommendedJobs.append(Jobs(job['ID'], job['Title'], job['Company'], job['Location'], salary,
                                        job['Summary'], applyLink))
            i=i+1;

        db = connection.Jobs
        jobs = db.jobsDetail
        for jobId in recommendedJobIDsUsingALS:
            if i==6:
                break;
            job = jobs.find_one({"userassignedId": jobId})
            recommendedJobs.append(Jobs(job['userassignedId'], job['JobTitle'], job['JobCompany'], job['JobLocation'], job['JobSalary'],
                                        job['JobSummary'], job['JobApplyLink']))
            i=i+1;

        print(recommendedJobs)

        return render(request, 'jobs.html', {"jobList": recommendedJobs, "isStoredJob": True})
    else:
        return render(request, 'Signinform.html')

def findTopRatedJobs(request):
    if request.method == "POST":
        topRatedJobs = recommendationAlgos.topRatedJobs()
        recommendedJobs = []

        connection = MongoClient(port=27017)
        db = connection.Jobs
        jobs = db.jobsDetail
        i = 1
        for jobId in topRatedJobs:
            if i == 6:
                break;
            job = jobs.find_one({"userassignedId": jobId})
            recommendedJobs.append(Jobs(job['userassignedId'], job['JobTitle'], job['JobCompany'], job['JobLocation'], job['JobSalary'],
                                        job['JobSummary'], job['JobApplyLink']))
            i = i + 1;

        print(recommendedJobs)

        return render(request, 'jobs.html', {"jobList": recommendedJobs, "isStoredJob": True})

    else:
        return render(request, 'Signinform.html')
