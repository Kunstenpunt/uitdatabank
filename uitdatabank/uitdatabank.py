from requests import get
from requests_oauthlib import OAuth1
from configparser import ConfigParser
from codecs import open
from os.path import dirname
from uitdatabank.searchresults import SearchResults


class UiTdatabank:
    """
    .. autosummary::
        :nosignatures:

        find
        construct_parameters_for_api_call
        construct_query
        construct_actor_query
        construct_production_query
        construct_event_query

    Very thin wrapper around UiTdatabank API v2, offering a simple way of authorizing and sending REST requests.

    Settings for authentication are given in a configuration file, e.g.
    ::

        [oauth]
        app_key = BAAC107B-632C-46C6-A254-13BC2CE19C6C
        app_secret = ec9a0e8c2cdc52886bc545e14f888612
        user_token =
        user_secret =

        [uitdatabank]
        url = https://www.uitid.be/uitid/rest/searchv2/search

    :param path_to_settings_file: a file in which the settings, such as oauth credentials and api url, are made explicit
    :param test: a boolean that can be set to True (default: False) so that only a limited amount of results is returned for test purposes

    :return: an UiTdatabank wrapper that can be used to query the database, whose results will be returned as an :mod:`SearchResults <uitdatabank.searchresults.SearchResults>` object

    You would simply initialize the class as follows:

    >>> udb = UiTdatabank("settings.cfg")

    Then, you could search by either constructing the query yourself, e.g. by looking for a concert in the city of Gent:

    >>> params = udb.construct_parameters_for_api_call({"q": "concert", "fq": "city:Gent"})
    >>> searchresults = udb.find(params)

    Or by relying on some of the helper functions, e.g. to look for an event that takes place in Brussels:

    >>> params = udb.construct_event_query([("city", "Brussel")])
    >>> searchresults = udb.find(params)

    Because writing queries like that is tedious, shortcut requests will be collected in a child class :mod:`Shortcuts <uitdatabank.shortcuts.Shortcuts>`, for recurring queries.
    """

    def __init__(self, path_to_settings_file, test=False):
        self.__settings = ConfigParser()
        self.__test = test
        self.__settings.read(path_to_settings_file)
        self.__auth = OAuth1(self.__settings["oauth"]["app_key"],
                             self.__settings["oauth"]["app_secret"],
                             self.__settings["oauth"]["user_token"],
                             self.__settings["oauth"]["user_secret"])
        self.__url = self.__settings["uitdatabank"]["url"]
        self.__headers = {'Accept': 'application/json'}
        self.event_query_fields = self.__get_supported_fields("/resources/supported_event_query_fields.txt")
        self.production_query_fields = self.__get_supported_fields("/resources/supported_production_query_fields.txt")
        self.actor_query_fields = self.__get_supported_fields("/resources/supported_actor_query_fields.txt")
        self.query_parameter_fields = self.__get_supported_fields("/resources/supported_query_parameter_fields.txt")

    @staticmethod
    def __get_supported_fields(textfile):
        """
        Parses a textfile in which supported field names are listed line by line.

        :param textfile: path to a textfile with supported fields

        :return: list of supported fields
        """
        with open(dirname(__file__) + textfile, "r", "utf-8") as f:
            return [item.strip() for item in f.readlines()]

    def find(self, parameters):
        """
        Main find method that makes the actual api call.

        :param parameters: the full query, containing the q, fq, etc. fields

        :return: An uitdatabank searchresults object

        One of the examples in the API documentation is to look for items that contain the word "concert" and that take place in Gent:

        >>> params = udb.construct_parameters_for_api_call({"q": "concert", "fq": "city:Gent"})
        >>> searchresults = udb.find(params)
        """
        return SearchResults(get(self.__url, auth=self.__auth, params=parameters, headers=self.__headers).text)

    def construct_parameters_for_api_call(self, kwargs):
        """
        Validates the query parameter fields against the API allowed fields, and constructs a query that can be send to the API

        :param kwargs: a dictionary containing all the parameters for the query

        :return: a dictionary of parameters that can be sent to the API by using the :func:`find` method

        >>> udb.construct_parameters_for_api_call({"q": "city:Brussels", "fq":"type:event", "z": "wrong key"})
        ValueError: Not a correct query parameter: z

        .. note::
           We are only supporting the following fields: 'q', 'fq', 'rows' and 'past'. This means that the user can not use start, sort, group, pt, sfield, d, facetField, transform and datetype.
           Sorting, grouping and transform will be provided in :mod:`SearchResults <uitdatabank.searchresults.SearchResults>`.
           datetype-like functionality will be provided in :mod:`Shortcuts <uitdatabank.shortcuts.Shortcuts>`.
           Geographical search and faceted search are under consideration.
        """
        out = {}
        for key, value in kwargs.items():
            if key in self.query_parameter_fields:
                out[key] = value
            else:
                raise ValueError("Not a correct query parameter: " + key)
        return out

    @staticmethod
    def construct_query(supported_fields, kvs_with_bools):
        """
        Validates a specific type of query against a list of supported fields

        :param supported_fields: a list of fields that is supported in the given type of query
        :param kvs_with_bools: a list of (key, value) tuples, potentially with booleans in between, that will be rewritten to a query

        :return: a string that can be passed to "q" in the api call

        The kvs_with_bools parameter defines the query, the supported_fields parameter is a list of fields that can be passed to the API

        (key, value) tuples define a search for a (field, search term)

        >>> udb.construct_query(udb.event_query_fields, [("city", "Gent")])
        "city:Gent"

        You can put a boolean operator string in between (key, value) tuples

        >>> udb.construct_query(udb.event_query_fields, [("city", "Gent"), "AND", ("organisor_label", "Vooruit")])
        "city:Gent AND organisor_label:Vooruit"

        >>> udb.construct_query(udb.event_query_fields, [("city", "Gent"), "AND", "concert"])
        "city:Gent AND concert"
        """
        if len(kvs_with_bools) % 2 == 0:
            raise ValueError("Not a correct query")
        else:
            q = ""
            for i, item in enumerate(kvs_with_bools):
                if (i % 2) == 0 and isinstance(item, tuple) and len(item) == 2 and item[0] in supported_fields:
                    q += ":".join(item)
                elif (i % 2) == 0 and isinstance(item, str) and item not in ["AND", "OR", "NOT"]:
                    q += item
                elif (i % 2) == 0 and item not in ["AND", "OR", "NOT"] and len(kvs_with_bools) == 1:
                    q += item
                elif (i % 2) != 0 and item in ["AND", "OR", "NOT"]:
                    q += " " + item + " "
                else:
                    raise ValueError("Not a correct query")
            return q

    def construct_production_query(self, search_terms_and_booleans):
        """
        Construct a query for productions

        :param search_terms_and_booleans: the search operation in the form of a list of (field, value) tuples, booleans, or full text searches, cf :func:`construct_query`

        :return: (a string that can be passed to "q" in the api call, a string that can be passed to "fq" in the call), this output fits :func:`find`
        """
        return self.construct_query(self.production_query_fields, search_terms_and_booleans), "type:production"

    def construct_event_query(self, key_value_tuples_with_booleans):
        """
        Construct a query for events

        :param key_value_tuples_with_booleans: a list of fields that is supported in the given type of query

        :return: (a string that can be passed to "q" in the api call, a string that can be passed to "fq" in the call), this output fits :func:`find`

        Query for an event that takes place in BXL and that somewhere contains the word 'jazz':

        >>> q, fq = udb.construct_event_query([("city", "Brussel"), "AND", "jazz"])
        >>> params = udb.construct_parameters_for_api_call({"q": q, "fq": fq})
        >>> searchresults = udb.find(params)
        """
        return self.construct_query(self.event_query_fields, key_value_tuples_with_booleans), "type:event"

    def construct_actor_query(self, key_value_tuples_with_booleans):
        """
        Construct a query for actors

        :param key_value_tuples_with_booleans: a list of fields that is supported in the given type of query

        :return: (a string that can be passed to "q" in the api call, a string that can be passed to "fq" in the call), this output fits :func:`find`
        """
        return self.construct_query(self.actor_query_fields, key_value_tuples_with_booleans), "type:actor"
