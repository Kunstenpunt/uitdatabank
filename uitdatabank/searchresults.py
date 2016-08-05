from datetime import datetime, timedelta
from json import loads
from uitdatabank.event import Event


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
                event = Event(item)
                when_from_event = event.get_when_from_event()[1]
                if when_from_event < earliest_moment:
                    earliest_moment = when_from_event
                    soonest_event = item
        return soonest_event

    def get_events(self):
        for item in self.results["rootObject"]:
            if "event" in item:
                event = Event(item)
                yield dict([event.get_title_from_event(),
                            event.get_long_description_from_event(),
                            event.get_when_from_event()])
