class CallbackAlert(Exception):
    def __init__(self, message: str, show_alert: bool = False, **kw):
        super(CallbackAlert, self).__init__(message)
        self.show_alert = show_alert
        self.message = message
        self.kw = kw
