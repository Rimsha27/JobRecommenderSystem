# def configureSpark(spark_home=None, pyspark_python=None):
#     os.environ['HADOOP_HOME'] = "C:/opt/spark/spark-2.2.1-bin-hadoop2.7/Hadoop/"
#     spark_home = "C:/opt/spark/spark-2.2.1-bin-hadoop2.7/"
#     os.environ['SPARK_HOME'] = spark_home
#
#     # Add the PySpark directories to the Python path:
#     sys.path.insert(1, os.path.join(spark_home, 'python'))
#     sys.path.insert(1, os.path.join(spark_home, 'python', 'pyspark'))
#     sys.path.insert(1, os.path.join(spark_home, 'python', 'build'))
#
#     # If PySpark isn't specified, use currently running Python binary:
#     pyspark_python = pyspark_python or sys.executable
#     os.environ['PYSPARK_PYTHON'] = pyspark_python
#     os.environ["PYSPARK_SUBMIT_ARGS"] = ("--packages org.mongodb.spark:mongo-spark-connector_2.11:2.2.0 pyspark-shell")
#
# try:
#     configureSpark()
# except:
#     print("Could not configure Spark")
#
# from pyspark import SparkContext
# from pyspark import SparkConf
# from pyspark.sql import SQLContext
# from pyspark.mllib.feature import HashingTF, IDF
# from pyspark.ml.feature import HashingTF, IDF, Normalizer, StopWordsRemover, RegexTokenizer, Word2Vec
# from pyspark.ml.feature import BucketedRandomProjectionLSH
# from pyspark.ml.linalg import Vectors
# from pyspark.sql.functions import col
# import pyspark.sql.functions as psf
# from pyspark.sql import Row
# import pandas as pd
# from sklearn.feature_extraction.text import TfidfVectorizer
# from scipy import spatial
# from operator import attrgetter
# from pyspark.mllib.linalg.distributed import IndexedRow, IndexedRowMatrix
# from pyspark.mllib.recommendation import ALS, Rating
# from pyspark.sql.types import *
#
# conf = SparkConf()
# conf.setMaster("local")
# conf.setAppName("spark_wc")
# sc = SparkContext(conf=conf)
# sqlContext = SQLContext(sc)

def contentBasedRecommendations(userId):
    # jobDataFrame = sqlContext.read.format("com.mongodb.spark.sql.DefaultSource").option("uri","mongodb://localhost:27017/JobDatabase.Jobs").load()
    # resumeDataFrame = sqlContext.read.format("com.mongodb.spark.sql.DefaultSource").option("uri","mongodb://localhost:27017/ResumeDatabase.Person").load()
    #
    # regexJobTokenizer = RegexTokenizer(inputCol="Job Data", outputCol="words", pattern="\\W")
    # regexResumeTokenizer = RegexTokenizer(inputCol="Profile Data", outputCol="words", pattern="\\W")
    #
    # tokenizedJobDataFrame = regexJobTokenizer.transform(jobDataFrame)
    # tokenizedResumeDataFrame = regexResumeTokenizer.transform(resumeDataFrame)
    #
    # remover = StopWordsRemover(inputCol="words", outputCol="filtered")
    #
    # processedJobDataFrame =remover.transform(tokenizedJobDataFrame)
    # processedResumeDataFrame = remover.transform(tokenizedResumeDataFrame)
    #
    # processedJobDataFrame=processedJobDataFrame.select("ID", "filtered")
    # processedResumeDataFrame =processedResumeDataFrame.select("ID", "filtered")
    #
    # hashingTF = HashingTF(inputCol="filtered", outputCol="rawFeatures", numFeatures=20)
    # featurizedJobDataFrame = hashingTF.transform(processedJobDataFrame)
    # featurizedResumeDataFrame = hashingTF.transform(processedResumeDataFrame)
    # #featurizedJobDataFrame.show(truncate=False)
    # #featurizedResumeDataFrame.show(truncate=False)
    #
    # idf = IDF(inputCol="rawFeatures", outputCol="features")
    # idfJobModel = idf.fit(featurizedJobDataFrame)
    # idfResumeModel = idf.fit(featurizedResumeDataFrame)
    #
    # rescaledJobData = idfJobModel.transform(featurizedJobDataFrame)
    # rescaledResumeData = idfResumeModel.transform(featurizedResumeDataFrame)
    #
    # normalizer = Normalizer(inputCol="features", outputCol="norm")
    # dataJ = normalizer.transform(rescaledJobData)
    # dataR = normalizer.transform(rescaledResumeData)
    # dataJ.show(truncate=False)
    # dataR.show(truncate=False)
    #
    #
    # dot_udf = psf.udf(lambda x, y: float(x.dot(y)))
    # SimilarityDataFrame=dataR.alias("Resume").crossJoin(dataJ.alias("Job")) \
    #     .select(
    #     psf.col("Resume.ID").alias("ResumeID"),
    #     psf.col("Job.ID").alias("JobID"),
    #     dot_udf("Resume.norm", "Job.norm").alias("Cosine Similarity")) \
    #     .sort("ResumeID", "JobID")
    #
    # ResumeOneRecommendations=SimilarityDataFrame.where(SimilarityDataFrame.ResumeID==userId)
    # OrderedResumeOneRecommendations=ResumeOneRecommendations.sort("Cosine Similarity", ascending=False).collect()
    recommendedJobs = []
    # i=0
    # for x in OrderedResumeOneRecommendations:
    #     recommendedJobs.append(x['JobID'])
    #     print(x)
    #     if i is 5:
    #         break
    #     i += 1

    return recommendedJobs


def ALSrecommendations(userId):
    # explicitRatings = sqlContext.read.format("com.mongodb.spark.sql.DefaultSource").option("uri",
    #                                                                                        "mongodb://localhost:27017/ExplicitFeedback.reviews").load()
    finalRecommendations = []
    # try:
    #     ratings = explicitRatings.rdd.map(lambda x: Rating(int(x[2]), \
    #                                                        int(x[1]), float(x[0])))
    #     # Setting up the parameters for ALS
    #     rank = 5  # Latent Factors to be made
    #     numIterations = 10  # Times to repeat process
    #     # Create the model on the training data
    #     model = ALS.train(ratings, rank, numIterations)
    #
    #     print("\nTop 10 recommendations:")
    #     recommendations = model.recommendProducts(int(userId), 10)
    #     #Why ALS would not produce any recommendation, maybe user has not rated a job and does not exist in the matrix
    #
    #     recommendedJobs = []
    #     for recommendation in recommendations:
    #         recommendedJobs.append(str(recommendation[1]) + "+" + str(recommendation[2]))
    #         print(str(recommendation[1]) + \
    #               " score " + str(recommendation[2]))
    #
    #     # convert the recommendations into dataframe
    #     recommendedJobsRdd = sc.parallelize(recommendedJobs).map(lambda x: x.split('+')).map(lambda x: Row(x[0], x[1]))
    #     recommendedJobsDF = recommendedJobsRdd.toDF()
    #     recommendedJobsDF = recommendedJobsDF.selectExpr("_1 as Jobid", "_2 as score")
    #
    #     # Subtract the jobs user has already rated
    #     ratedJobs = explicitRatings[explicitRatings['Userid'] == userId].select(['Jobid']).distinct()
    #     recommendedJobs = recommendedJobsDF.select(['Jobid']).distinct().subtract(ratedJobs)
    #
    #     recommendedJobs = recommendedJobsDF.join(recommendedJobs, "Jobid", "right_outer").orderBy('score', ascending=False)
    #     i = 1
    #     for x in recommendedJobs.collect():
    #         finalRecommendations.append(int(x.Jobid))
    #         if i == 5:
    #             break;
    #         i = i + 1
    #     print(finalRecommendations)
    # except:
    #     print("no recommendation from ALS")
    return finalRecommendations

def topRatedJobs():
    # implicitRatings = sqlContext.read.format("com.mongodb.spark.sql.DefaultSource").option("uri",
    #                                                                                     "mongodb://localhost:27017/ImplicitFeedback.reviews").load()
    recommendedJobs = []
    # if implicitRatings.count():
    #     implicitRatings = implicitRatings.select('Jobid', 'ImplicitRating')
    #     implicitRatings = implicitRatings.withColumn("Jobid", implicitRatings["Jobid"].cast(IntegerType()))
    #     print(implicitRatings.show())
    #     implicitRatings = implicitRatings.rdd.reduceByKey(lambda a, b: a + b).toDF().selectExpr("_1 as Jobid",
    #                                                                                             "_2 as ImplicitRating")
    #     implicitRatings = implicitRatings.orderBy('ImplicitRating', ascending=False)
    #     i = 1
    #     for x in implicitRatings.collect():
    #         recommendedJobs.append(int(x.Jobid))
    #         if i == 5:
    #             break;
    #         i = i + 1
    #     print(recommendedJobs)
    return recommendedJobs