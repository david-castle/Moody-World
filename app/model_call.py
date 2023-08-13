from app import model_newsapi, model_gnewsapi, model_processing

class RunModels():

    def __init__(self):
        print("Call API models.")

    def modelCall(self):
        na1 = model_newsapi.NewsApi()
        na1.ScoreAndSave()
        na2 = model_gnewsapi.GNewsApi()
        na2.ScoreAndSave()
        p = model_processing.ProcessingFrame()
        p.readingFrames()
        p.applyToFrame()