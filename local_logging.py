import os.path
import datetime as dt
from datetime import datetime



class Logging:

    def __init__(self):
        if os.path.isdir('logs') is False: #Create directory 'log' and respective log files if not already present
            os.mkdir('logs')
            self.error_log = open("logs/errors_log.txt", "w+")
            self.comment_log = open("logs/comment_log.txt", "w+")
            self.url_log = open("logs/url_log.txt", "w+")
        else:
            self.error_log = open("logs/errors_log.txt", "w+")
            self.comment_log = open("logs/comment_log.txt", "w+")
            self.url_log = open("logs/url_log.txt", "w+")



    def logError(self, e):
        curr_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f  ')[:-4]
        err = curr_time + str(e) +"\n"
        self.error_log.write(err)
        print(err)

    def logComment(self, reddit_info, c):
        curr_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f  ')[:-4]
        comm = curr_time + reddit_info + " : " + str(c) +"\n"
        self.comment_log.write(comm)
        print("Commented")


    def logURLChecked(self, url):
        print("Here")
        curr_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f  ')[:-4]
        comm = curr_time + " : " + str(url) + "\n"
        self.url_log.write(comm)












