class _BaseE(Exception):
    def __init__(self, err_response, expr, msg):
        self.expr = expr
        self.msg = msg
        self.response = err_response

class LeafLinkClientRequestError(_BaseE):
    pass

class LeafLinkClient5XXError(_BaseE):
    pass
