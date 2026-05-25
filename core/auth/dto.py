from core.auth.user.user_dto import UserResponse

class AuthResponse:
    access_token: str
    refresh_token: str
    user: UserResponse

    def __init__(self, user: UserResponse, access_token: str, refresh_token: str):
        self.user = user
        self.access_token = access_token
        self.refresh_token = refresh_token