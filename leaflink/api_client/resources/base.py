from ..models.base import Model
from ..client.base import APIResource as _APIResource


class API(object):
    def __init__(self, company, api_key, base_url):
        self.company = company
        self.api_key = api_key
        self.base_url = base_url

    def resource(self, model, method, uri, path_param=None, **data):
        _uri = self._parse_uri(uri, path_param)
        configs = None

        if self.api_key:
            configs = {
                "API_KEY": self.api_key,
                "BASE_URL": self.base_url
            }

        req = lambda q, d=None: getattr(
            _APIResource(query=q,
                         data=d,
                         endpoint=_uri,
                         user_configs=configs),
            method)()

        return model(api_request=req, **data)

    def _parse_uri(self, uri, _id=None):
        if "{company}" in uri:
            uri = uri.format(company=self.company)

        if _id:
            uri = uri.format(id=_id)

        return uri

