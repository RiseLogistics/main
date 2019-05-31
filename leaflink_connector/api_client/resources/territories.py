from .base import API, Model


class TerritoriesQuery(Model):
    _QUERY_ = ["limit", "offset"]


class TerritoriesCreateUpdate(Model):
    _SCHEMA_ = {
        "shipping_charge"   : ("int",   Model.OPTIONAL),
        "name"              : ("str",   Model.OPTIONAL),
        "rank"              : ("int",   Model.OPTIONAL),
        "regions"           : ("list",  Model.OPTIONAL),
        "state"             : ("dict",  Model.OPTIONAL),
        "sales_reps"        : ("list",  Model.OPTIONAL),
    }


class Territories(API):

    @property
    def list(self):
        return self.resource(
            model=TerritoriesQuery,
            uri="/{company}/territories/",
            method="get"
        )

    def create(self, **data):
        return self.resource(
            model=TerritoriesCreateUpdate,
            uri="/{company}/territories/",
            method="post",
            **data
        )

    def get_by_id(self, territory_id):
        return self.resource(
            model=TerritoriesQuery,
            uri="/{company}/territories/{id}/",
            path_param=territory_id,
            method="get"
        )

    def delete(self, territory_id):
        return self.resource(
            model=TerritoriesQuery,
            uri="/{company}/territories/{id}/",
            path_param=territory_id,
            method="delete"
        )

    def patch(self, territory_id, **data):
        return self.resource(
            model=TerritoriesCreateUpdate,
            uri="/{company}/territories/{id}/",
            path_param=territory_id,
            method="patch",
            **data
        )

    def put(self, territory_id, **data):
        return self.resource(
            model=TerritoriesCreateUpdate,
            uri="/{company}/territories/{id}/",
            path_param=territory_id,
            method="put",
            **data
        )

