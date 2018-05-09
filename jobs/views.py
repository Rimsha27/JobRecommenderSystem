import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from pymongo import MongoClient
from accounts import models
from . import recommendationAlgos

_MONGODB_USER = "hjrsfyp"
_MONGODB_PASSWD = "123456"
_MONGODB_HOST = "ds259089.mlab.com:59089"
_MONGODB_NAME = "jrs"
mongo_uri = 'mongodb://%s:%s@%s/%s' % (_MONGODB_USER, _MONGODB_PASSWD, _MONGODB_HOST, _MONGODB_NAME)
client = MongoClient(mongo_uri)
db = client.jrs

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

    def as_json(self):
        return dict(id=self.id,
            jobTitle=self.jobTitle,
            jobCompany=self.jobCompany,
            jobLocation=self.jobLocation,
            jobSalary=self.jobSalary,
            jobSummary=self.jobSummary,
            jobLink=self.jobLink)

#This is called after successful Sign in or Sign up
def jobsviewing(request):
    return findTopRatedJobs(request)

#This function displays a job detail and stores the click on read more as implicit feedback
def displayingJobDetail(request):
    if request.user.is_authenticated:
        jobs = request.session.get('jobs', None)
        implicitFbCollection = db.ImplicitFeedbackCollection

        jobDetailsCollection = db.RatedJobsCollection

        # Here I will first get the Job id from the Hidden Text Box
        jobId = [key for key in request.POST if key.startswith("jobId")]

        # Getting the username
        username = request.user.username

        # Now retrieving the Django object corresponding to it from the Sqlite3 Database
        UserRecord = models.signupModel.objects.filter(email=username)

        # Getting the Job
        jobId = jobId[0].split("+")
        jobId = int(jobId[1])

        jobToBeStored = None
        print("The job to be saved", jobId)
        for job in jobs:
            if job['id'] == jobId:
                jobToBeStored = job

        if jobDetailsCollection.count() == 0 and jobToBeStored is not None:
            print("Job Rated Database is empty")
            jobId = 15001
            Job = {
                'userassignedId': jobId,
                'JobTitle': jobToBeStored['jobTitle'],
                'JobCompany': jobToBeStored['jobCompany'],
                'JobLocation': jobToBeStored['jobLocation'],
                'JobSalary': jobToBeStored['jobSalary'],
                'JobSummary': jobToBeStored['jobSummary'],
                'JobApplyLink': jobToBeStored['jobLink'],
            }
            result = jobDetailsCollection.insert_one(Job)
            print("Job inserted and job id is ", jobId)
        elif jobToBeStored is not None:
            print("Job Rated Database is not empty")

            # This covers the scenario when a user has clicked a searched job and then he again searches and the same job appers, the jobId will be local so we are searching on job title
            jobsData = jobDetailsCollection.find_one({"JobTitle": jobToBeStored['jobTitle']})
            if jobsData is not None:
                jobId = jobsData['userassignedId']
                print("Job is already stored in Job Rated Database", jobId)
            else:
                print("Job is not stored in Job Rated Database")
                no_of_documents = jobDetailsCollection.count();
                jobId = 15000 + no_of_documents + 1
                Job = {
                    'userassignedId': jobId,
                    'JobTitle': jobToBeStored['jobTitle'],
                    'JobCompany': jobToBeStored['jobCompany'],
                    'JobLocation': jobToBeStored['jobLocation'],
                    'JobSalary': jobToBeStored['jobSalary'],
                    'JobSummary': jobToBeStored['jobSummary'],
                    'JobApplyLink': jobToBeStored['jobLink'],
                }
                result = jobDetailsCollection.insert_one(Job)
                print("Job inserted and job id is ", jobId)
        else:
            return render(request, 'jobs.html', {"jobList": jobs, "popJobs": "The job does not exist"})

        #If the user has rated the job before
        feed_back_of_user = implicitFbCollection.find_one({"Userid": UserRecord[0].idformongo, "Jobid": jobId})
        #If he hadn't
        if feed_back_of_user is None:
            print("The user has not rated the job before!")
            implicit_feedback_count = 1
            Feedback = {
                'Userid': UserRecord[0].idformongo,
                'Jobid': jobId,
                'ImplicitRating': implicit_feedback_count
            }
            result = implicitFbCollection.insert_one(Feedback)
            print("Feedback saved.")
        #f he had
        else:
            # This means that the User has already opened this job and gave implplicit rating
            # So increasing the previous count Would do the job
            # Incrementing the Job Implicit Rating
            print("The user has rated the job before!")
            implicitFbCollection.update(
                {'Userid': UserRecord[0].idformongo, 'Jobid': jobId},
                {
                    "$inc": {"ImplicitRating": 1}
                }
            )
            print("Feedback updated.")
        return render(request, 'jobsDetail.html', {"jobsDetail": jobToBeStored})
    else:
        return render(request, 'Signinform.html')

#It retrieves the job based on keyword and location and shows them to the user
def jobsretrieving(request):
    if request.user.is_authenticated:
        jobs = []

        id_temp = ""
        jobTitle_temp = ""
        jobCompany_temp = ""
        jobLocation_temp = ""
        jobSalary_temp = ""
        jobSummary_temp = ""
        jobLink_temp = ""

        desc = request.POST['keyword']
        j = 0
        start = 0

        while start is not 20:
            r = requests.get("https://www.indeed.com/jobs?q=" + desc + "&start=" + str(start),
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

                    jobTitle = jobSoup.find("b", {"class": "jobtitle"})
                    if jobTitle is not None:
                        jobData = jobTitle.text

                        jobTitle_temp = jobTitle.text

                        jobCompany = jobSoup.find("span", {"class": "company"})

                        if jobCompany:
                            jobData = jobData + " " + jobCompany.text
                            jobCompany_temp = jobCompany.text

                        jobLocation = jobSoup.find("span", {"class": "location"})

                        if jobLocation:
                            jobData = jobData + " " + jobLocation.text
                            jobLocation_temp = jobLocation.text

                        jobSalary = jobSoup.find("span", {"class": "no-wrap"})
                        if jobSalary:
                            jobData = jobData + " " + jobSalary.text
                            jobSalary_temp = jobSalary.text

                        jobApplyLink = jobSoup.find("a", {"class": "view_job_link view-apply-button blue-button"})
                        if jobApplyLink:
                            jobApplyLink = "https://www.indeed.com" + jobApplyLink.get("href")
                            jobLink_temp = jobApplyLink
                            # print(jobApplyLink)

                        jobSummary = jobSoup.find("span", {"class": "summary"})
                        if jobSummary:
                            jobData = jobData + " " + jobSummary.text
                            jobSummary_temp = jobSummary.text

                        id_temp = j
                        jobs.append(Jobs(id_temp, jobTitle_temp, jobCompany_temp, jobLocation_temp, jobSalary_temp,
                                         jobSummary_temp, jobLink_temp))
                        j += 1

        serializableJobs = [job.as_json() for job in jobs]
        request.session['jobs'] = serializableJobs
        return render(request, 'jobs.html', {"jobList": jobs, "popJobs": ""})
    else:
        return render(request, 'Signinform.html')

def saveExplicitRating(request):
    if request.user.is_authenticated:
        jobs = request.session.get('jobs', None)

        ExplicitFbCollection = db.ExplicitFeedbackCollection
        jobDetailsCollection = db.RatedJobsCollection

        actual_star_number_and_job_number = request.POST.get('star')

        # Getting the username
        username = request.user.username

        # Now retrieving the Django object corresponding to it from the Sqlite3 Database
        UserRecord = models.signupModel.objects.filter(email=username)

        # Getting the JobTitle
        Number = actual_star_number_and_job_number.split("+")
        print("Star Rating is", Number[1])
        print("Job id is ", Number[2])

        jobId = int(Number[2])

        jobToBeStored = None
        print("The job to be saved", jobId)
        popJobs = ""
        if jobId >= 15000:
            popJobs = "Most Popular Jobs"
        for job in jobs:
            if job['id'] == jobId:
                jobToBeStored = job

        if jobToBeStored is not None:
            print(jobToBeStored['jobTitle'])
            jobTitle = jobToBeStored['jobTitle']
            jobsData = jobDetailsCollection.find_one({"JobTitle": jobTitle})
            print(jobsData['userassignedId'])
            jobId = jobsData['userassignedId']

            # If the user has rated the job before
            feed_back_of_user = ExplicitFbCollection.find_one({"Userid": UserRecord[0].idformongo, "Jobid": jobId})

            # If he hadn't
            if feed_back_of_user is None:
                print("The user has not rated the job")
                Feedback = {
                    'Userid': UserRecord[0].idformongo,
                    'Jobid': jobId,
                    'ExplicitRating': Number[1]
                }
                result = ExplicitFbCollection.insert_one(Feedback)
                print("Feedback Saved")
            #If he had, update the rating
            else:
                print("The user has rated the job")
                ExplicitFbCollection.update(
                    {"Jobid": jobId, "Userid": UserRecord[0].idformongo},
                    {"$set": {"ExplicitRating": Number[1]}}
                )
                print("Feedback Updated")
            return render(request, 'jobs.html', {"jobList": jobs, "popJobs": popJobs})
        else:
            return render(request, 'jobs.html', {"jobList": jobs, "popJobs": "The job does not exist"})
    else:
        return render(request, 'Signinform.html')

def findTopRatedJobs(request):
    if request.user.is_authenticated:

        recommendedJobs = []
        implicitRatingsCollection = db.ImplicitFeedbackCollection
        jobsCollection = db.RatedJobsCollection
        topRatedJobs = implicitRatingsCollection.aggregate(
            [
                { "$group": {"_id": "$Jobid", "total": { "$sum": "$ImplicitRating"}}},
                { "$sort": {"total": -1}}
            ]
        )
        i=0
        for job in topRatedJobs:
            if i == 10:
                break
            i = i + 1
            id = job['_id']
            print(id)
            jobDetails = jobsCollection.find_one({"userassignedId": id})
            recommendedJobs.append(
                Jobs(jobDetails['userassignedId'], jobDetails['JobTitle'], jobDetails['JobCompany'], jobDetails['JobLocation'], jobDetails['JobSalary'],
                     jobDetails['JobSummary'], jobDetails['JobApplyLink']))
        serializableJobs = [job.as_json() for job in recommendedJobs]
        request.session['jobs'] = serializableJobs
        return render(request, 'jobs.html', {"jobList": recommendedJobs, "popJobs": "Most Popular Jobs"})

    else:
        return render(request, 'Signinform.html')

def backButton(request):
    if request.user.is_authenticated:
        jobs = request.session.get('jobs', None)
        popJobs = ""
        if next(iter(jobs))['id'] >= 15000:
            popJobs = "Most Popular Jobs"
        return render(request, 'jobs.html', {"jobList": jobs, "popJobs": popJobs})
    else:
        return render(request, 'Signinform.html')


# This was in case when we were handling three kind of jobs(jobs from ALS, jobs from content based, searched jobs) to be rated all having different local IDs
# if jobDetailsCollection.count() == 0:
#     print("Job Rated Database is empty")
#     if jobType == "False":
#         print("The job is the searched job")
#         jobToBeStored = jobs[jobId - 1]
#     else:
#         print("The job is the stored job")
#         jobsData = storedJobsCollection.find_one({"ID": jobId})
#         try:
#             salary = jobsData.Salary
#         except:
#             salary = ""
#         try:
#             applyLink = jobsData.ApplyLink
#         except:
#             applyLink = ""
#         jobToBeStored = Jobs(jobsData['ID'], jobsData['Title'], jobsData['Company'], jobsData['Location'],
#                              salary, jobsData['Summary'], applyLink)
#     jobId = 15001
#     Job = {
#         'userassignedId': jobId,
#         'JobTitle': jobToBeStored.jobTitle,
#         'JobCompany': jobToBeStored.jobCompany,
#         'JobLocation': jobToBeStored.jobLocation,
#         'JobSalary': jobToBeStored.jobSalary,
#         'JobSummary': jobToBeStored.jobSummary,
#         'JobApplyLink': jobToBeStored.jobLink,
#     }
#     result = jobDetailsCollection.insert_one(Job)
#     print("inserted")
#
# #Jobs Database is not empty
# else:
#     # check if the job already exists or not
#     print("Job collection is not empty")
#     print(jobId)
#     jobsData = jobDetailsCollection.find_one({"userassignedId": jobId})
#     print(jobsData)
#
#     #If does not exists, retrieve the number of jobs and assign count+1 as jobId
#     if jobsData is None:
#         if jobType == "False":
#             print("The job is the searched job")
#             jobToBeStored = jobs[jobId - 1]
#             jobsData = jobDetailsCollection.find_one({"JobTitle": jobToBeStored.jobTitle})
#
#             #This covers the scenario when a user has clicked a searched job and then he again searches and the same job appers, the jobId will be local so we are searching on job title
#             if jobsData is not None:
#                 jobId = jobsData['userassignedId']
#             else:
#                 no_of_documents = jobDetailsCollection.count();
#                 jobId = 15000 + no_of_documents + 1
#                 Job = {
#                     'userassignedId': jobId,
#                     'JobTitle': jobToBeStored.jobTitle,
#                     'JobCompany': jobToBeStored.jobCompany,
#                     'JobLocation': jobToBeStored.jobLocation,
#                     'JobSalary': jobToBeStored.jobSalary,
#                     'JobSummary': jobToBeStored.jobSummary,
#                     'JobApplyLink': jobToBeStored.jobLink,
#                 }
#                 result = jobDetailsCollection.insert_one(Job)
#                 print("inserted")
#         else:
#             print("The job is the stored job")
#             jobsData = storedJobsCollection.find_one({"ID": jobId})
#             try:
#                 salary = jobsData.Salary
#             except:
#                 salary = ""
#             try:
#                 applyLink = jobsData.ApplyLink
#             except:
#                 applyLink = ""
#             jobToBeStored = Jobs(jobsData['ID'], jobsData['Title'], jobsData['Company'], jobsData['Location'],
#                                  salary,
#                                  jobsData['Summary'], applyLink)
#             jobsData = jobDetailsCollection.find_one({"JobTitle": jobToBeStored.jobTitle})
#
#             # This covers the scenario when a user has clicked a recommended job(from CBR) and then he again clicks, its id will be the one from storedJobs so we'll search based on jobTitle
#             if jobsData is not None:
#                 jobId = jobsData['userassignedId']
#             else:
#                 no_of_documents = jobDetailsCollection.count();
#                 jobId = 15000 + no_of_documents + 1
#                 Job = {
#                     'userassignedId': jobId,
#                     'JobTitle': jobToBeStored.jobTitle,
#                     'JobCompany': jobToBeStored.jobCompany,
#                     'JobLocation': jobToBeStored.jobLocation,
#                     'JobSalary': jobToBeStored.jobSalary,
#                     'JobSummary': jobToBeStored.jobSummary,
#                     'JobApplyLink': jobToBeStored.jobLink,
#                 }
#                 result = jobDetailsCollection.insert_one(Job)
#                 print("inserted")
#     else:
#         jobId = jobsData['userassignedId']
#         jobToBeStored = Jobs(jobsData['userassignedId'], jobsData['JobTitle'], jobsData['JobCompany'], jobsData['JobLocation'],
#                              jobsData['JobSalary'], jobsData['JobSummary'], jobsData['JobApplyLink'])
#


#Explicit Rating
# jobsData = jobDetailsCollection.find_one({"userassignedId": jobId})
# print(jobsData)
#
# # If does not exists, retrieve the number of jobs and assign count+1 as jobId
# if jobsData is None:
#
#     if jobType == "False":
#         jobToBeStored = jobs[jobId - 1]
#         jobTitle = jobToBeStored.jobTitle
#         jobsData = jobDetailsCollection.find_one({"JobTitle": jobTitle})
#         jobId = jobsData['userassignedId']
#     else:
#         storedJobsCollection = db.StoredJobsCollection
#
#         jobsData = storedJobsCollection.find_one({"ID": jobId})
#         jobTitle = jobsData['Title']
#         jobsData = jobDetailsCollection.find_one({"JobTitle": jobTitle})
#         jobId = jobsData['userassignedId']

# def recommendjobs(request):
#     if request.user.is_authenticated:
#         username = request.user.username
#         UserRecord = models.signupModel.objects.filter(email=username)
#         ID = UserRecord[0].idformongo
#         recommendedJobIDsUsingContent = recommendationAlgos.contentBasedRecommendations(ID)
#         recommendedJobIDsUsingALS = recommendationAlgos.ALSrecommendations(ID)
#         print(recommendedJobIDsUsingContent)
#         print(recommendedJobIDsUsingALS)
#
#         jobs = db.StoredJobsCollection
#         recommendedJobs = []
#         i=0
#         for jobId in recommendedJobIDsUsingContent:
#             if i==3:
#                 break;
#             job = jobs.find_one({"ID": jobId})
#             print(job)
#             try:
#                 salary = job['Salary']
#             except:
#                 salary = ""
#             try:
#                 applyLink = job['ApplyLink']
#             except:
#                 applyLink = ""
#             recommendedJobs.append(Jobs(job['ID'], job['Title'], job['Company'], job['Location'], salary,
#                                         job['Summary'], applyLink))
#             i=i+1;
#
#         jobs = db.RatedJobsCollection
#         for jobId in recommendedJobIDsUsingALS:
#             if i==6:
#                 break;
#             job = jobs.find_one({"userassignedId": jobId})
#             recommendedJobs.append(Jobs(job['userassignedId'], job['JobTitle'], job['JobCompany'], job['JobLocation'], job['JobSalary'],
#                                         job['JobSummary'], job['JobApplyLink']))
#             i=i+1;
#
#         return render(request, 'jobs.html', {"jobList": recommendedJobs, "popJobs": ""})
#     else:
#         return render(request, 'Signinform.html')

