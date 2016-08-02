from datetime import datetime, timedelta
from json import loads
from uitdatabank.eventparser import EventParser


class SearchResults:
    """
    Initializes the uitdatabank search results

    :param results_string: the json output of the uitdatabank json

    :return: None
    """

    def __init__(self, results_string):
        self.results = loads(results_string)

    def get_soonest_event(self):
        earliest_moment = datetime.today() + timedelta(weeks=100)
        soonest_event = None
        for item in self.results["rootObject"]:
            if "event" in item:
                when_from_event = EventParser.get_when_from_event(item)[1]
                if when_from_event < earliest_moment:
                    earliest_moment = when_from_event
                    soonest_event = item
        return soonest_event

    def get_events(self):
        for item in self.results["rootObject"]:
            if "event" in item:
                yield dict([EventParser.get_title_from_event(item),
                            EventParser.get_long_description_from_event(item),
                            EventParser.get_when_from_event(item)])
