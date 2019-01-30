# From user 'jfs' on StackOverflow: https://stackoverflow.com/users/4279/jfs
# StackOverflow thread containing the response that included the below method:
# https://stackoverflow.com/a/28607501


from datetime import datetime, time as datetime_time, timedelta


def time_diff(start, end):
    if isinstance(start, datetime_time): # convert to datetime
        assert isinstance(end, datetime_time)
        start, end = [datetime.combine(datetime.min, t) for t in [start, end]]
    if start <= end: # e.g., 10:33:26-11:15:49
        return end - start
    else: # end < start e.g., 23:55:00-00:25:00
        end += timedelta(1) # +day
        assert end > start
        return end - start