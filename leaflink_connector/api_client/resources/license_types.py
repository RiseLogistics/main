from .base import API, Model


class LicenseTypesQuery(Model):
    _QUERY_ = [
        "limit",
        "offset"
    ]


class LicenseTypes(API):

    @property
    def list(self):
        return self.resource(
            model=LicenseTypesQuery,
            uri="/{company}/license-types/",
            method="get"
        )

    @property
    def crm(self):
        return self.resource(
            model=LicenseTypesQuery,
            uri="/{company}/license-types/crm/",
            method="get"
        )

    def get_by_id(self, license_type_id):
        return self.resource(
            model=LicenseTypesQuery,
            uri="/{company}/license-types/{id}/",
            path_param=license_type_id,
            method="get"
        )
