from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from pandas._libs import json
from pymongo import MongoClient

from accounts import models
from accounts.models import signupModel, workexperienceModel, Education


# from accounts.models import signupModel
def signup(request):
    if request.method == "POST":
        try:
            User.objects.get(username=request.POST['username'])
            return render(request, 'Signupform.html', {'error': 'Email has already been taken!Try Another Mail'})
        except User.DoesNotExist:

            # Here the stuff will also be saved in the MongoDB in order to generate the Recommendation
            # for the User which has just signed in

            # client = MongoClient('localhost:27017')
            # db = client.ResumeDatabase
            #
            # # Inserting the ID of the Relevant User
            # no_of_documents = db.Person.count();
            # ID = no_of_documents + 1
            #
            # db.Person.insert_one(
            #     {
            #         "ID": ID,
            #     })
            #
            # # Making Profile Data Variable for TF-IDF Comparison
            # # Initially profileData String is populated with Position Applied
            # profileData = "not mentioned"
            #
            # db.Person.update(
            #     {"ID": ID},
            #     {"$set": {"Position Applied": "not mentioned"}}
            # )
            #
            # # Populating the Profile Data with the Userlocation which is the concatenation of
            # # of the city and the country
            # profileData += " " + request.POST['City'] + request.POST['Country']
            #
            # db.Person.update(
            #     {"ID": ID},
            #     {"$set": {"User Location": request.POST['City'] + request.POST['Country']}}
            # )
            #
            # # Populating the profileData with the objective the user has entered in the box
            # profileData += " " + request.POST['textarea']
            #
            # db.Person.update(
            #     {"ID": ID},
            #     {"$set": {"Objective": request.POST['textarea']}}
            # )
            #
            #
            #
            #
            # listofcompanies1 = request.POST.getlist('Company[]')
            # listofpositions1 = request.POST.getlist('Position[]')
            # listofstartdates1 = request.POST.getlist('startdates[]')
            # listofenddates1 = request.POST.getlist('enddates[]')
            # listofDescription1 = request.POST.getlist('Descriptions[]')
            #
            # for i in range(0, len(listofcompanies1)):
            #     profileData += " " + listofcompanies1[i]
            #     profileData += " " + listofpositions1[i]
            #     profileData += " " + listofDescription1[i]
            #
            #     db.Person.update(
            #         {"ID": ID},
            #         {"$push": {"Work Experience": {
            #             "ExperienceID": i,
            #             "Company": listofcompanies1[i],
            #             "Title": listofpositions1[i],
            #             "Dates": listofstartdates1[i] + ' to ' + listofenddates1[i],
            #             "Description": listofDescription1[i]
            #         }}}
            #     )
            #
            # listofdegrees1 = request.POST.getlist('degreenames[]')
            # listofinstitution1 = request.POST.getlist('institution[]')
            # listofstartdates2 = request.POST.getlist('startdates1[]')
            # listofenddates2 = request.POST.getlist('enddates1[]')
            #
            # for i in range(0, len(listofdegrees1)):
            #     profileData += " " + listofinstitution1[i]
            #     profileData += " " + listofdegrees1[i]
            #
            #     db.Person.update(
            #         {"ID": ID},
            #         {"$push": {"Education": {
            #             "EducationID": i,
            #             "School": listofinstitution1[i],
            #             "Title": listofdegrees1[i],
            #             "Dates": listofstartdates2[i] + ' to ' + listofenddates2[i],
            #         }}}
            #     )
            #
            # skills_coming = request.POST.getlist('skills[]')
            # interests_coming = request.POST.getlist('interests[]')
            #
            # for i in range(0, len(skills_coming)):
            #     profileData += " " + skills_coming[i]
            #     db.Person.update(
            #         {"ID": ID},
            #         {"$push": {"Skills": {
            #             "Skill": skills_coming[i],
            #         }}}
            #     )
            #
            # temp1 = ""
            # for i in range(0, len(interests_coming)):
            #     if i == len(interests_coming) - 1:
            #         temp1 = temp1 + interests_coming[i]
            #     else:
            #         temp1 = temp1 + interests_coming[i] + ','
            #
            #
            #
            #
            # profileData += " " + temp1
            # db.Person.update(
            #     {"ID": ID},
            #     {"$set": {"Additional Information": temp1}}
            # )
            #
            # db.Person.update(
            #     {"ID": ID},
            #     {"$set": {"Profile Data": profileData}}
            # )
            #
            #
            user1 = User.objects.create_user(request.POST['username'], password=request.POST['password'])

            #Creating the user Signup Model



            signUpModel = signupModel.objects.create(user=user1, name=request.POST['name'],
                                                     dateofbirth=request.POST['dob'],
                                                     gender=request.POST.get('gender', None),
                                                     email=request.POST['username'],
                                                     password=request.POST['password'],
                                                     skills=json.dumps(request.POST.getlist('skills[]')),
                                                     interests=request.POST.getlist('interests[]'),
                                                     objectivestatement=request.POST['textarea'],
                                                     country=request.POST['Country'], city=request.POST['City'],
                                                     idformongo=ID)

            signUpModel.save()
            #
            # # Getting the list from the input tags
            listofcompanies = request.POST.getlist('Company[]')
            listofpositions = request.POST.getlist('Position[]')
            listofstartdates = request.POST.getlist('startdates[]')
            listofenddates = request.POST.getlist('enddates[]')

            listofdegrees = request.POST.getlist('degreenames[]')
            listofinstitution = request.POST.getlist('institution[]')
            listofstartdate1 = request.POST.getlist('startdates1[]')
            listofenddate1 = request.POST.getlist('enddates1[]')
            #
            ArrayContainingExperiencesObject = []
            # Creating objects for the users
            for i in range(0, len(listofcompanies)):
                temp = workexperienceModel.objects.create(id=None,
                                                          company=listofcompanies[i],
                                                          position=listofpositions[i],
                                                          startDate=listofstartdates[i],
                                                          endDate=listofenddates[i],
                                                          UserExperience=signUpModel)
                ArrayContainingExperiencesObject.append(temp)

            for j in range(1, len(ArrayContainingExperiencesObject)):
                ArrayContainingExperiencesObject[j].save()

            ArrayContainingEducationObject = []
            for i in range(0, len(listofdegrees)):
                temp1 = Education.objects.create(id=None, degree=listofdegrees[i], institution=listofinstitution[i],
                                                 startdateedu=listofstartdate1[i],
                                                 enddateedu=listofenddate1[i], UserEducation=signUpModel)
                ArrayContainingEducationObject.append(temp1)

            for k in range(1, len(ArrayContainingEducationObject)):
                ArrayContainingEducationObject[k].save()

                # Setting the session
            login(request, user1)
            UserRecord = models.signupModel.objects.filter(email=request.POST['username'])
            return render(request, 'jobs.html')
            # return render(request, 'MainPage.html', {'UserRecord': UserRecord})
    else:
        return render(request, 'Signupform.html')


def loginview(request):
    if request.method == "POST":
        user = authenticate(username=request.POST['username1'], password=request.POST['password1'])
        if user is not None:
            login(request, user)
            username = None
            if request.user.is_authenticated:
                return render(request, 'jobs.html')

        else:
            return render(request, 'Signinform.html', {'error': 'The user name and password didn\'t match.'})
    else:
        return render(request, 'Signinform.html')


def logoutview(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')
    else:
        return render(request, 'Signupform.html')


def mainpageview(request):
    print(request.user)
    print(request.user.username)

    flag = False
    flag1 = False

    if request.user.is_authenticated:
        username = request.user.username

        UserRecord = models.signupModel.objects.filter(email=username)
        UserEducations = models.Education.objects.filter(UserEducation=UserRecord[0])
        UserExperiences = models.workexperienceModel.objects.filter(UserExperience=UserRecord[0])

        skills = UserRecord[0].skills.replace('"', '').replace('[', '').replace(']', '').split(",")
        interests1 = UserRecord[0].interests.replace("'", "").replace(" ", "").replace("[", "").replace("]", "").split(
            ",")
        if UserRecord[0].gender == 'male':
            flag = True
        else:
            flag1 = True

        return render(request, 'MainPage.html', {'UserRecord': UserRecord,
                                                 'UserEducation': UserEducations,
                                                 'UserExperience': UserExperiences,
                                                 "flag": flag,
                                                 "flag1": flag1,
                                                 "Skills": skills,
                                                 "Interests": interests1
                                                 })
    else:
        return render(request, 'Signinform.html')


def editprofile(request):
    # Now here i ll retrieve all the credentials of the user from the
    # database and will display them on the page
    flag = False
    flag1 = False
    if request.user.is_authenticated:
        username = request.user.username

        UserRecord = models.signupModel.objects.filter(email=username)
        UserEducations = models.Education.objects.filter(UserEducation=UserRecord[0])
        UserExperiences = models.workexperienceModel.objects.filter(UserExperience=UserRecord[0])

        skills = UserRecord[0].skills.replace('"', '').replace('[', '').replace(']', '').split(",")
        interests1 = UserRecord[0].interests.replace("'", "").replace(" ", "").replace("[", "").replace("]", "").split(
            ",")

        if UserRecord[0].gender == 'male':
            flag = True
        else:
            flag1 = True

        return render(request, 'EditProfile.html', {'UserRecord': UserRecord,
                                                    'UserEducation': UserEducations,
                                                    'UserExperience': UserExperiences,
                                                    "flag": flag,
                                                    "flag1": flag1,
                                                    "Skills": skills,
                                                    "Interests": interests1
                                                    })
    else:
        return render(request, 'Signinform.html')

def updateinformation(request):
    flag = False
    flag1 = False
    if request.method == "POST":
        if request.user.is_authenticated():
            username = request.user.username
            if username == request.POST['email']:
                # Deleting the models from the signupModel,Django provided model
                # Deleting the Signup model automatically deletes the WorkExperiences,Educations Model
                # print(request.user.username)

                logout(request)

                User.objects.filter(username=username).delete()
                print(request.user.username)

                # signupModel.objects.filter(email=username).delete()

                # Creating Everything new from here on
                user1 = User.objects.create_user(request.POST['email'], password=request.POST['password'])
                print(request.user.username)

                # Creating the user Signup Model
                signUpModel = signupModel.objects.create(user=user1, name=request.POST['name'],
                                                         dateofbirth=request.POST['dob'],
                                                         gender=request.POST.get('gender', None),
                                                         email=request.POST['email'],
                                                         password=request.POST['password'],
                                                         skills=json.dumps(request.POST.getlist('skills[]')),
                                                         interests=request.POST.getlist('interests[]'),
                                                         objectivestatement=request.POST['objstat'],
                                                         country=request.POST['country'], city=request.POST['City'])

                signUpModel.save()

                # Getting the list from the input tags
                listofcompanies = request.POST.getlist('Company[]')
                listofpositions = request.POST.getlist('Position[]')
                listofstartdates = request.POST.getlist('startdates[]')
                listofenddates = request.POST.getlist('enddates[]')

                listofdegrees = request.POST.getlist('degreenames[]')
                listofinstitution = request.POST.getlist('institution[]')
                listofstartdate1 = request.POST.getlist('startdates1[]')
                listofenddate1 = request.POST.getlist('enddates1[]')

                ArrayContainingExperiencesObject = []
                # Creating objects for the users
                for i in range(0, len(listofcompanies)):
                    temp = workexperienceModel.objects.create(id=None,
                                                              company=listofcompanies[i],
                                                              position=listofpositions[i],
                                                              startDate=listofstartdates[i],
                                                              endDate=listofenddates[i],
                                                              UserExperience=signUpModel)
                    ArrayContainingExperiencesObject.append(temp)

                for j in range(1, len(ArrayContainingExperiencesObject)):
                    ArrayContainingExperiencesObject[j].save()

                ArrayContainingEducationObject = []
                for i in range(0, len(listofdegrees)):
                    temp1 = Education.objects.create(id=None, degree=listofdegrees[i], institution=listofinstitution[i],
                                                     startdateedu=listofstartdate1[i],
                                                     enddateedu=listofenddate1[i], UserEducation=signUpModel)
                    ArrayContainingEducationObject.append(temp1)

                for k in range(1, len(ArrayContainingEducationObject)):
                    ArrayContainingEducationObject[k].save()

                login(request, user1)

                return render(request, 'jobs.html',
                              {'error': "Bio Updated Successfully"})
            else:
                flag = username_present(request.POST['email'])
                if flag == True:
                    username = request.user.username
                    UserRecord = models.signupModel.objects.filter(email=username)
                    UserEducations = models.Education.objects.filter(UserEducation=UserRecord)
                    UserExperiences = models.workexperienceModel.objects.filter(UserExperience=UserRecord)
                    skills = UserRecord[0].skills.replace('"', '').replace('[', '').replace(']', '').split(",")
                    interests1 = UserRecord[0].interests.replace("'", "").replace(" ", "").replace("[", "").replace("]",
                                                                                                                    "").split(
                        ",")

                    if UserRecord[0].gender == 'male':
                        flag = True
                    else:
                        flag1 = True

                    return render(request, 'EditProfile.html', {'UserRecord': UserRecord,
                                                                'UserEducation': UserEducations,
                                                                'UserExperience': UserExperiences,
                                                                "flag": flag,
                                                                "flag1": flag1,
                                                                "Skills": skills,
                                                                "Interests": interests1,
                                                                "error": "Email already taken please try a different email!"
                                                                })
                else:

                    logout(request)

                    # Deleting the models from the signupModel,Django provided model
                    # Deleting the Signup model automatically deletes the WorkExperiences,Educations Model
                    User.objects.filter(username=username).delete()
                    #   signupModel.objects.filter(email=username).delete()

                    # Creating Everything new from here on
                    user1 = User.objects.create_user(request.POST['email'], password=request.POST['password'])
                    # Creating the user Signup Model
                    signUpModel = signupModel.objects.create(user=user1, name=request.POST['name'],
                                                             dateofbirth=request.POST['dob'],
                                                             gender=request.POST.get('gender', None),
                                                             email=request.POST['email'],
                                                             password=request.POST['password'],
                                                             skills=json.dumps(request.POST.getlist('skills[]')),
                                                             interests=request.POST.getlist('interests[]'),
                                                             objectivestatement=request.POST['objstat'],
                                                             country=request.POST['country'], city=request.POST['City'])

                    signUpModel.save()

                    # Getting the list from the input tags
                    listofcompanies = request.POST.getlist('Company[]')
                    listofpositions = request.POST.getlist('Position[]')
                    listofstartdates = request.POST.getlist('startdates[]')
                    listofenddates = request.POST.getlist('enddates[]')

                    listofdegrees = request.POST.getlist('degreenames[]')
                    listofinstitution = request.POST.getlist('institution[]')
                    listofstartdate1 = request.POST.getlist('startdates1[]')
                    listofenddate1 = request.POST.getlist('enddates1[]')

                    ArrayContainingExperiencesObject = []
                    # Creating objects for the users
                    for i in range(0, len(listofcompanies)):
                        temp = workexperienceModel.objects.create(id=None,
                                                                  company=listofcompanies[i],
                                                                  position=listofpositions[i],
                                                                  startDate=listofstartdates[i],
                                                                  endDate=listofenddates[i],
                                                                  UserExperience=signUpModel)
                        ArrayContainingExperiencesObject.append(temp)

                    for j in range(1, len(ArrayContainingExperiencesObject)):
                        ArrayContainingExperiencesObject[j].save()

                    ArrayContainingEducationObject = []
                    for i in range(0, len(listofdegrees)):
                        temp1 = Education.objects.create(id=None, degree=listofdegrees[i],
                                                         institution=listofinstitution[i],
                                                         startdateedu=listofstartdate1[i],
                                                         enddateedu=listofenddate1[i], UserEducation=signUpModel)
                        ArrayContainingEducationObject.append(temp1)

                    for k in range(1, len(ArrayContainingEducationObject)):
                        ArrayContainingEducationObject[k].save()
                    login(request, user1)

                    return render(request, 'jobs.html',
                                  {'error': "Bio Updated Successfully"})

        return render(request, 'EditProfile.html')
    else:
        return render(request, 'Signinform.html')

def username_present(username):
    try:
        User.objects.get(username=username)
        return True
    except User.DoesNotExist:
        return False


def sendtohome(request):
    if request.method == "POST":
        return render(request, "jobs.html")
    else:
        return render(request, 'Signinform.html')