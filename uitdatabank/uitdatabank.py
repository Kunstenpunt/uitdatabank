from requests import get
from requests_oauthlib import OAuth1
from configparser import ConfigParser
from codecs import open
from os.path import dirname
from uitdatabank.searchresults import SearchResults


class UiTdatabank:
    """
    Main class for making API calls to UiTdatabank API v2
    """

    def __init__(self, path_to_settings_file, test=False):
        """
        Wrapper around UiTdatabank API v2

        :param path_to_settings_file: a file in which the settings, such as oauth credentials and api url, are made explicit
        :param test: a boolean that can be set to True (default: False) so that only a limited amount of results is returned for test purposes

        :return: an UiTdatabank wrapper that can be used to query the database, whose results will be returned as an UiTdatabankSearchresults object
        """
        self.settings = ConfigParser()
        self.test = test
        self.settings.read(path_to_settings_file)
        self.auth = OAuth1(self.settings["oauth"]["app_key"],
                           self.settings["oauth"]["app_secret"],
                           self.settings["oauth"]["user_token"],
                           self.settings["oauth"]["user_secret"])
        self.url = self.settings["uitdatabank"]["url"]
        self.headers = {'Accept': 'application/json'}
        self.supported_event_query_fields = \
            self.__get_supported_fields("/resources/supported_event_query_fields.txt")
        self.production_query_fields = self.__get_supported_fields("/resources/supported_production_query_fields.txt")
        self.actor_query_fields = self.__get_supported_fields("/resources/supported_actor_query_fields.txt")
        self.query_parameter_fields = self.__get_supported_fields("/resources/supported_query_parameter_fields.txt")

    @staticmethod
    def __get_supported_fields(textfile):
        """
        Parses a textfile in which supported field names are listed line by line

        :param textfile: path to a textfile with supported fields

        :return: list of supported fields
        """
        with open(dirname(__file__) + textfile, "r", "utf-8") as f:
            return [item.strip() for item in f.readlines()]

    def find(self, prms):
        """
        Main find method that makes the actual api call

        :param prms: the full query, containing the q, fq, etc. fields

        :return: An uitdatabank searchresults object
        """
        return SearchResults(get(self.__url, auth=self.__auth, params=parameters, headers=self.__headers).text)

    def construct_query_parameters(self, kwargs):
        """
        Validates the query parameter fields, and constructs a query that can be send to the API

        :param kwargs: a dictionary containing all the parameters for the query, e.g. {"q": "city:Brussels", "fq":"type:event"}

        :return: a dictionary of parameters that can be sent to the API, e.g. using the find() method
        """
        out = {}
        for key, value in kwargs.items():
            if key in self.query_parameter_fields:
                out[key] = value
            else:
                raise ValueError("Not a correct query parameter")
        return out

    @staticmethod
    def __construct_query(supported_fields, kvs_with_bools=list):
        """
        Validates a specific type of query against a list of supported fields

        :param supported_fields: a list of fields that is supported in the given type of query
        :param kvs_with_bools: a list of (key, value) tuples, potentially with booleans in between, that will be rewritten to a query

        :return: a string that can be passed to "q" in the api call
        """
        if len(kvs_with_bools) % 2 == 0:
            raise ValueError("Not a correct query")
        else:
            q = ""
            for i, item in enumerate(kvs_with_bools):
                if (i % 2) == 0 and isinstance(item, tuple) and len(item) == 2 and item[0] in supported_fields:
                    q += ":".join(item)
                elif (i % 2) == 0 and item not in ["AND", "OR", "NOT"] and len(kvs_with_bools) == 1:
                    q += item
                elif (i % 2) != 0 and item in ["AND", "OR", "NOT"]:
                    q += " " + item + " "
                else:
                    raise ValueError("Not a correct query")
            return q

    def construct_production_query(self, key_value_tuples_with_booleans=list):
        """
        Construct a query for a production

        :param key_value_tuples_with_booleans: a list of fields that is supported in the given type of query

        :return: (a string that can be passed to "q" in the api call, a string that can be passed to "fq" in the call)
        """
        return self.__construct_query(self.production_query_fields, key_value_tuples_with_booleans), "type:production"

    def construct_event_query(self, key_value_tuples_with_booleans=list):
        """
        Construct a query for events

        :param key_value_tuples_with_booleans: a list of fields that is supported in the given type of query

        :return: (a string that can be passed to "q" in the api call, a string that can be passed to "fq" in the call)
        """
        return self.__construct_query(self.supported_event_query_fields, key_value_tuples_with_booleans), "type:event"

    def construct_actor_query(self, key_value_tuples_with_booleans=list):
        """
        Construct a query for actors

        :param key_value_tuples_with_booleans: a list of fields that is supported in the given type of query

        :return: (a string that can be passed to "q" in the api call, a string that can be passed to "fq" in the call)
        """
        return self.__construct_query(self.actor_query_fields, key_value_tuples_with_booleans), "type:actor"

