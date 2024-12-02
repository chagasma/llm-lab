class InvalidRequestError(Exception):
    def __init__(self, message="Invalid request"):
        super().__init__(message)


class EnvironmentVariableError(Exception):
    def __init__(self, message="Environment variable failed"):
        super().__init__(message)
