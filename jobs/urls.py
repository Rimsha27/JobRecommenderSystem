from django.conf.urls import url
from jobs import views

app_name = 'jobs'

urlpatterns = [
    url(r'^$', views.jobsviewing, name="jobs"),
    url(r'^actualjobs/',views.jobsretrieving,name="jobsretrieve"),
    url(r'^recommendedjobs/', views.recommendjobs, name="recommendjobs"),
    url(r'^jobsDetails/',views.displayingJobDetail,name = "jobsdisplay"),
    url(r'^savedJobsRatings',views.saveExplicitRating,name = "saveExplicitRating"),
    url(r'^findTopRatedJobs',views.findTopRatedJobs,name = "topratedjobs")

]
