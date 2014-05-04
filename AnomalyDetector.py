#import nupic
import model_params
from nupic.frameworks.opf.modelfactory import ModelFactory
from nupic.encoders.scalar import ScalarEncoder
from nupic.encoders.date import DateEncoder
from nupic.encoders.sdrcategory import SDRCategoryEncoder
from nupic.data.inference_shifter import InferenceShifter
import numpy
import foursquare
import datetime

class Checkin():
    def __init__(self, latitude, longitude, time, likes, people, categories):
        self.latitude=latitude
        self.longitude=longitude
        self.time=time
        self.likes=likes
        self.people=people
        self.categories=categories

class FourSquareAnomalyDetector():
    def __init__(self):
        self.lat = ScalarEncoder(name='latitude',  w=3, n=100, minval=-90, maxval=90,
                        periodic=False)
        self.long= ScalarEncoder(name='longitude',  w=3, n=100, minval=-180, maxval=180,
                        periodic=True)
        self.timeenc= DateEncoder(season=0, dayOfWeek=1, weekend=3, timeOfDay=5)
        self.likes = ScalarEncoder(name='likes',  w=3, n=50, minval=0, maxval=100000,
                        periodic=False)
        self.people = ScalarEncoder(name='numpeople',  w=3, n=20, minval=0, maxval=100,
                        periodic=False)
        self.categories = SDRCategoryEncoder(n=87, w=3, categoryList = None,
                             name="cats", verbosity=0)
        self.run()

    def run(self):
        check1=Checkin(10,100,datetime.datetime.utcnow(),12,5,"cafe")
        check2=Checkin(10,100,datetime.datetime.utcnow(),12,5,"cafe")
        check3=Checkin(10,100,datetime.datetime.utcnow(),12,5,"cafe")
        check4=Checkin(10,100,datetime.datetime.utcnow(),12,5,"cafe")
        check5=Checkin(10,100,datetime.datetime.utcnow(),12,5,"cafe")
        check6=Checkin(10,100,datetime.datetime.utcnow(),12,5,"cafe")
        check7=Checkin(10,100,datetime.datetime.utcnow(),12,5,"cafe")
        check8=Checkin(10,100,datetime.datetime.utcnow(),12,5,"cafe")
        list_of_unencoded_checkins=[check1,check2,check3,check4,check5,check6,check7,check8]
        list_of_encoded_checkins=[]
        for check in list_of_unencoded_checkins:
            print check
            list_of_encoded_checkins.append(self.encode(check))
        print self.LastAnomalyScore(list_of_encoded_checkins)


    def createModel(self):
        return ModelFactory.create(model_params.MODEL_PARAMS)

    def encode(self, checkin):
        print checkin
        latenc=self.lat.encode(checkin.latitude)
        longenc=self.long.encode(checkin.longitude)
        timenc=self.timeenc.encode(checkin.time)
        likeenc=self.likes.encode(checkin.likes)
        peoplenc=self.people.encode(checkin.people)
        for cat in checkin.categories:
            try:
                catenc=numpy.logical_or(catenc,self.categories.encode(cat))
            except:
                catenc=self.categories.encode(cat)
        checkinsdr=numpy.concatenate((latenc,longenc,timenc,likeenc,peoplenc,catenc))
        print checkinsdr
        print type(checkinsdr)
        return checkinsdr

    def LastAnomalyScore(self, checkin_list):
        model = self.createModel()
        model.enableInference({'predictedField': 'checkin'})
        last_anomaly = 0
        for i, record in enumerate(checkin_list, start=1):
            modelInput = {"checkin": record}
            result = model.run(modelInput)
            anomalyScore = result.inferences['anomalyScore']
            last_anomaly = anomalyScore
        return last_anomaly


foursq = FourSquareAnomalyDetector()


