from .base import Model


class Response(Model):
    _SCHEMA_ = {
        "count"         : ("int",  Model.OPTIONAL),
        "next"          : ("str",  Model.OPTIONAL),
        "previous"      : ("str",  Model.OPTIONAL),
        "results"       : ("list", Model.OPTIONAL),
        "status_code"   : ("int",  Model.REQUIRED)
    }
