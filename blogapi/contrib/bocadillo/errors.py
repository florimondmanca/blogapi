from bocadillo import errors


class HTTPError(errors.HTTPError):
    def __init__(self, *args, headers: dict = None, **kwargs):
        super().__init__(*args, **kwargs)
        if headers is None:
            headers = {}
        self.headers = headers


errors.HTTPError = HTTPError
