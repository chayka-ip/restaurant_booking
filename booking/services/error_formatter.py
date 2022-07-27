from rest_framework.response import Response


class ErrorFormatter:
    def __init__(self, error_text="", status=None):
        self.error_text = error_text
        self.status = status

    @property
    def as_response(self):
        d = {"error": self.error_text}
        r = Response(d)
        if self.status:
            r.status_code = self.status
        return r
