#import nupic

#from nupic.frameworks.opf.modelfactory import ModelFactory
#from nupic.data.inference_shifter import InferenceShifter
import foursquare


class FourSquareAnomalyDetector():
    def __init__(self, token):
        self.token = token
        self.client = foursquare.Foursquare(access_token=self.token)
        self.run()


    def run(self):
        foursquareself = self.client.users()
        self.friend_checkins = []
        for friend in self.client.users.friends():
            self.friend_checkins.append(self.return_checkins(friend))
        print self.friend_checkins

    def return_checkins(self, id):
        self.checkins=[]
        for checkin in self.client.users.all_checkins(id):
            self.checkins.append(checkin)
        return self.checkins




#    def detect(self):
#        model = ModelFactory.create(self.model_params.MODEL_PARAMS)
#        model.enableInference({"predictedField": "field"})
#        i = 1
#        for datapoint in self.dataset:
#            result = model.run({"field": checkin})
#            prediction = result.inferences['multiStepBestPredictions'][i]
#            i = i + 1
#        return (result.inferences['anomalyScore'])

foursq=FourSquareAnomalyDetector('5ISV1HHDSEFX44Y4H34GYC55020Q3HST55EUL2BDDNIFXKCV')


