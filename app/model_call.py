import model_fox 
import model_guardian 
import model_nbc 
import model_newsapi

class RunModels():

    def __init__(self):
        print("Gettin started")

    def modelCall(self):
        print("Starting it")
        na1 = model_newsapi.NewsApi()
        print("Instantiated")
        na1.getInfo()
        na1.createDateFrame()
        return "done"