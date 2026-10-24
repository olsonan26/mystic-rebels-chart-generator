class ChartError(Exception):
    def __init__(self, code: str, message: str, **details):
        super().__init__(message)
        self.code, self.message, self.details = code, message, details

    def record(self):
        return {'code':self.code,'message':self.message,'details':self.details}
