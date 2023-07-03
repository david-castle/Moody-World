import model_fox 
import model_guardian 
import model_nbc 

class RunModels():

    def __init__(self):
        print("Gettin started")

    def modelCall(self):
        print("Starting it")
        n1 = model_nbc.newsSoupNBC()
        f1 = model_fox.newsSoupFox()
        g1 = model_guardian.newsSoupGuardian()
        print("Instantiated")
        n1.getInfo()
        n1.cleanAll_Tags()
        n1.createDataFrame()
        f1.getInfoh2()
        f1.cleanAll_Tags_h2()
        f1.createDataFrame()
        g1.getInfo()
        g1.cleanAll_Tags()
        g1.createDataFrame()
        return "done"