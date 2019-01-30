import time
from ximilar.client import RecognitionClient




class Ximilar_Main:

    app_client = RecognitionClient(token="")
    task, status = app_client.get_task(task_id='')

    def __init__(self):
        app_client = RecognitionClient(token="")
        task, status = app_client.get_task(task_id='')

    def isImageTweet(self, image_url):  #Tries 3 times in the case that an error occurs with the API call

        for attempts in range(0, 2):
            try:
                result = self.task.classify([{"_url": image_url}])
                best_label = result['records'][0]['best_label']
                if best_label['name'] == 'twitter-sc':
                    return True
                else:
                    return False
            except Exception as e:
                print("Error using Ximilar: "+str(e))
                if attempts == 2:
                    return False
                else:
                    time.sleep(1)
