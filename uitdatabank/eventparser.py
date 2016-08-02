from datetime import datetime, timedelta


class EventParser:
    """
    Helper class to parse event documents in the json output of the UiTdatabank API v2
    """

    def __init__(self):
        self.test = "ahloha"

    def get_test(self):
        return self.test

    @staticmethod
    def get_when_from_event(event):
        """
        Fetches the dates and hours at which the event start (or started)

        :param event: the 'event' json document that is produced by the UiTdatabank v2 api

        :return: label, a python datetime objects indicating at what day and hour the event starts the earliest, with epoch = 0 if no result
        """
        if event["event"]["calendar"]["timestamps"]:
            return "when", min([datetime.fromtimestamp(ts["date"] / 1000.) +
                                timedelta(milliseconds=ts["timestart"] if ts["timestart"] else -3600000, hours=1)
                                for ts in event["event"]["calendar"]["timestamps"]["timestamp"]])
        elif event["event"]["calendar"]["periods"]:
            return "when", min([datetime.fromtimestamp(event["event"]["calendar"]["periods"]["period"]["datefrom"] /
                                                       1000.)])
        else:
            return "when", datetime(1970, 1, 1)

    @staticmethod
    def get_title_from_event(event):
        return "title", event["event"]["eventdetails"]["eventdetail"][0]["title"]

    @staticmethod
    def get_long_description_from_event(event):
        return "long description", event["event"]["eventdetails"]["eventdetail"][0]["longdescription"]
