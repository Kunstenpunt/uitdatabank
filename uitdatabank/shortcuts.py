from uitdatabank.uitdatabank import UiTdatabank


class Shortcuts(UiTdatabank):
    def __init__(self, path_to_settings_file, test):
        UiTdatabank.__init__(self, path_to_settings_file, test)

    def __find_upcoming_events_by_x(self, x, value):
        q, fq = self.construct_event_query([(x, value)])
        params = self.construct_parameters_for_api_call({'q': q, 'fq': fq, 'rows': 10 if self.__test else 10000, 'past': False})
        return self.find(params)
