from abc import abstractmethod


class DataOrErrorFromRequestData:
    def __init__(self, request):
        self.request = request
        self.error = None
        self.status = None
        self.data = None
        self._extract()

    @property
    def has_errors(self):
        return self.error is not None

    @abstractmethod
    def _extract(self):
        pass

    def get_data(self):
        """ Always returns valid data when has no errors """
        return self.data
