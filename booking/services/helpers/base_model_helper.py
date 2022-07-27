class BaselHelper:
    def __init__(self, request):
        self.request = request
        self.request_data = request.data
        self.user = request.user

    # ===== SERVICE METHODS =====

    def is_user_auth(self) -> bool:
        """ check if user is authenticated or not """
        if self.user.is_authenticated:
            return True
        return False

    def get_request_data_copy(self) -> dict:
        return self.request_data.copy()

    def get_user_email(self) -> str:
        if self.is_user_auth():
            return self.user.email
        return ''
