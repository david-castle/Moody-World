import os

class CleanUp():
    def __init__(self):
        print("Cleaning up.")

    def cleaning_temps(self):
        for folder, subfolders, files in os.walk('temp/'):
                    for file in files:
                        if file.endswith('.csv') or file.endswith('.txt'):
                            path = os.path.join(folder, file)
                            print('deleted : ', path)
                            os.remove(path)

    def cleaning_processed(self):
        if os.path.exists("processed_frame.csv"):
            os.remove("processed_frame.csv")
        else:
            pass