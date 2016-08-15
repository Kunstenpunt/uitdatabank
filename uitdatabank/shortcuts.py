from uitdatabank.uitdatabank import UiTdatabank


class Shortcuts(UiTdatabank):
    """
    .. autosummary::
        :nosignatures:

        find_upcoming_events_by_organiser_label
        find_upcoming_events_by_city_name

    The Shortcuts class offers a number of probably frequently queries to the UiTdatabank.
    A full typology of queries is being thought up, so for now there are only limited shortcuts available.
    Feel free to help thinking about a topology: https://github.com/ruettet/uitdatabank/issues/2

    :param path_to_settings_file: a file in which the settings, such as oauth credentials and api url, are made explicit
    :param test: a boolean that can be set to True (default: False) so that only a limited amount of results is returned for test purposes

    :return: an UiTdatabank wrapper that can be used to query the database, whose results will be returned as an :mod:`SearchResults <uitdatabank.searchresults.SearchResults>` object

    As an example, you could look for upcoming events in Brussels as follows:

    >>> udb_shortcuts = Shortcuts("settings.cfg")
    >>> upcoming_events_in_brussels = udb_shortcuts.find_upcoming_events_by_city_name("Brussel")
    >>> for event in upcoming_events_in_brussels.get_events():
    ...   print(event)

    # TODO to make this class a subclass of UiTdatabank is probably not the best design, I am still thinking about a better solution.
    Feel free to suggest a better design: https://github.com/ruettet/uitdatabank/issues/3
    """
    def __init__(self, path_to_settings_file, test):
        super(Shortcuts, self).__init__(path_to_settings_file, test)

    def __find_upcoming_events_by_x(self, x, value):
        q, fq = self.construct_event_query([(x, value)])
        params = self.construct_parameters_for_api_call({'q': q, 'fq': fq, 'rows': 10 if self._test else 10000, 'past': False})
        return self.find(params)

    def find_upcoming_events_by_organiser_label(self, organiser_label):
        """
        Finds upcoming events that are organised by a specific organization

        :param organiser_label: The full text label for an organization
        :return: :mod:`SearchResults <uitdatabank.searchresults.SearchResults>` object

        >>> udb_shortcuts = Shortcuts("settings.cfg")
        >>> upcoming_events_in_flagey = udb_shortcuts.find_upcoming_events_by_organiser_label("Flagey")
        >>> for event in upcoming_events_in_flagey.get_events():
        ...   print(event)

        """
        return self.__find_upcoming_events_by_x("organiser_label", organiser_label)

    def find_upcoming_events_by_city_name(self, city_name):
        """
        Finds upcoming events that are organised in a specific location

        :param city_name: Name of community where event takes place
        :return: :mod:`SearchResults <uitdatabank.searchresults.SearchResults>` object

        >>> udb_shortcuts = Shortcuts("settings.cfg")
        >>> upcoming_events_in_bxl = udb_shortcuts.find_upcoming_events_by_organiser_label("Brussel")
        >>> for event in upcoming_events_in_bxl.get_events():
        ...   print(event)
        """
        return self.__find_upcoming_events_by_x("city", city_name)
