from datetime import datetime, timedelta


class Event:
    """
    Helper class to parse event documents in the json output of the UiTdatabank API v2
    """
    def __init__(self, json_object):
        self.event = json_object

    def get_when_from_event(self):
        """
        Fetches the dates and hours at which the event start (or started)

        :param event: the 'event' json document that is produced by the UiTdatabank v2 api

        :return: label, a python datetime objects indicating at what day and hour the event starts the earliest, with epoch = 0 if no result
        """
        if self.event["event"]["calendar"]["timestamps"]:
            return "when", min([datetime.fromtimestamp(ts["date"] / 1000.) +
                                timedelta(milliseconds=ts["timestart"] if ts["timestart"] else -3600000, hours=1)
                                for ts in self.event["event"]["calendar"]["timestamps"]["timestamp"]])
        elif self.event["event"]["calendar"]["periods"]:
            return "when", min([datetime.fromtimestamp(self.event["event"]["calendar"]["periods"]["period"]["datefrom"] / 1000.)])
        else:
            return "when", datetime(1970, 1, 1)

    def get_title_from_event(self):
        return "title", self.event["event"]["eventdetails"]["eventdetail"][0]["title"]

    def get_long_description_from_event(self):
        return "long description", self.event["event"]["eventdetails"]["eventdetail"][0]["longdescription"]
