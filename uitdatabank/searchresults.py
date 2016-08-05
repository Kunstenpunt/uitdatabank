from datetime import datetime, timedelta
from json import loads
from uitdatabank.event import Event


class SearchResults:
    """
    .. autosummary::
        :nosignatures:

        get_soonest_event
        get_events

    The search results of a query on UiTdatabank are pure json, which is nice, but there should be some functionality to easily navigate this json file.
    The SearchResults class offers some functionalities.

    :param results_string: the json output of the uitdatabank json

    :return: None

    As an example, you could look for upcoming events in Brussels:

    >>> udb_shortcuts = Shortcuts("settings.cfg")
    >>> upcoming_events_in_brussels = udb_shortcuts.find_upcoming_events_by_city_name("Brussel")
    >>> for event in upcoming_events_in_brussels.get_events():
    ...   print(event)
    """

    def __init__(self, results_string):
        self.results = loads(results_string)

    def get_soonest_event(self):
        """
        This function gets the earliest event in the search results

        :return:
        """
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
