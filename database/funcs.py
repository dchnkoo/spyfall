import datetime as _date


class DBFuncs:

    @property
    def now_utc(self):
        return lambda: _date.datetime.now(_date.timezone.utc)


funcs = DBFuncs()
