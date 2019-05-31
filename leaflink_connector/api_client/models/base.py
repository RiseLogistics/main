

class Model(object):

    __slots__ = [
        "SCHEMA", "__dict__", "R_", "Q_"
    ]

    # Set a Model Schema field as OPTIONAL/REQUIRED
    class _OPT: pass
    class _REQ: pass

    OPTIONAL  = _OPT()
    REQUIRED  = _REQ()

    _SCHEMA_  = None
    _QUERY_   = {}

    def __init__(self, schema=None, api_request=None, **kwargs):
        self.SCHEMA = schema or self._SCHEMA_ or {}

        self.R_ = api_request
        self.Q_ = {}

        if self.SCHEMA is None:
            raise KeyError("Model Schema Not Set")

        if kwargs:
            self._setup(**kwargs)

    def load(self, _json):
        for k, v in _json.items():
            if isinstance(self._field_type(k), Model):
                v = self._field_type(k).load(v)

            self._set_attr(k, v)

        return self

    def dump(self, skip_none=True):
        results = {}
        for k, v in self._CONTAINER:
            if v is None and skip_none:
                continue

            if isinstance(v, Model):
                v = v.dump()

            results[k] = v

        return results

    def dump_all(self):
        return self.dump(skip_none=False)

    def query(self, validate=True, **kwargs):
        if not validate:
            return self._q(**kwargs)

        for k, v in kwargs.items():
            if k not in self._QUERY_:
                raise KeyError("Unexpected Query Keyword '{0}'".format(k))

        return self._q(**kwargs)

    def _q(self, **kwargs):
        self.Q_ = kwargs
        return self.run()

    def run(self, **kwargs):
        if self._CONTAINER:
            return self.R_(self.Q_, self.dump(), **kwargs)

        return self.R_(self.Q_, **kwargs)

    def _set_attr(self, key, val, validate_schema=False):
        if validate_schema:
            self._raise_if_required(key, val)

        setattr(self, key, val)

    def _raise_if_required(self, k, v):
        if v is None and self._is_field_required(k):
            raise KeyError("Key {0} must not be None".format(k))

        return False

    def _field_type(self, k):
        field_type, _ = self.SCHEMA.get(k, (None, None))
        return field_type

    def _is_field_required(self, k):
        _, is_required = self.SCHEMA[k]
        return isinstance(is_required, self._REQ)

    def _setup(self, **kwargs):
        for k, default in self.SCHEMA.items():
            v = kwargs.get(k, None)
            self._set_attr(k, v, validate_schema=True)

        return self

    @property
    def _CONTAINER(self):
        return self.__dict__.items()

    def __call__(self, *args, **kwargs):
        return self.run(**kwargs)
