
from .base import Model


class Error(Model):
    _SCHEMA_ = {
        "detail"        : ("str", Model.OPTIONAL),
        "status_code"   : ("int", Model.REQUIRED)
    }