from datetime import datetime, timedelta


def convert_date(timestamp, border):
    current = datetime.now().strftime("%Y-%m-%d")
    if border == "start":
        timestamp = timestamp if timestamp else current
        return "{} 00:00:00+0300".format(timestamp)
    if border == "end":
        timestamp = timestamp if timestamp else current
        return "{} 23:59:59+0300".format(timestamp)


def get_stop_date(stop_days):
    return (datetime.now() + timedelta(+stop_days)).strftime("%Y-%m-%d")
