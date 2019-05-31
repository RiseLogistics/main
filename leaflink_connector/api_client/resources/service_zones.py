from .base import API, Model


class ServiceZonesQuery(Model):
    _QUERY_ = [
        "limit",
        "offset",
        "search"
    ]


class ServiceZonesCreateUpdate(Model):
    _SCHEMA_ = {
        "name"          : ("str", Model.OPTIONAL),
        "description"   : ("str", Model.OPTIONAL),
        "id"            : ("int", Model.OPTIONAL)
    }


class ServiceZones(API):

    @property
    def list(self):
        return self.resource(
            model=ServiceZonesQuery,
            uri="/{company}/service-zones/",
            method="get"
        )

    def create(self, **data):
        return self.resource(
            model=ServiceZonesCreateUpdate,
            uri="/{company}/service-zones/",
            method="post",
            **data
        )

    def delete(self, service_zone_id):
        return self.resource(
            model=ServiceZonesQuery,
            uri="/{company}/service-zones/{id}/",
            path_param=service_zone_id,
            method="delete"
        )

    def get_by_id(self, service_zone_id):
        return self.resource(
            model=ServiceZonesQuery,
            uri="/{company}/service-zones/{id}/",
            path_param=service_zone_id,
            method="get"
        )

    def patch(self, service_zone_id, **data):
        return self.resource(
            model=ServiceZonesCreateUpdate,
            uri="/{company}/service-zones/{id}/",
            path_param=service_zone_id,
            method="patch",
            **data
        )

    def put(self, service_zone_id, **data):
        return self.resource(
            model=ServiceZonesCreateUpdate,
            uri="/{company}/service-zones/{id}/",
            path_param=service_zone_id,
            method="put",
            **data
        )

