from .base import API, Model


class CustomerStatusesQuery(Model):
    _QUERY_ = [
        "limit",
        "offset"
    ]


class CustomerStatusesCreateUpdate(Model):
    _SCHEMA_ = {
        "state"         : ("str",   Model.OPTIONAL),
        "is_stock"      : ("bool",  Model.OPTIONAL),
        "order"         : ("int",   Model.OPTIONAL),
        "description"   : ("str",   Model.OPTIONAL)
    }


class CustomerStatuses(API):

    @property
    def list(self):
        return self.resource(
            model=CustomerStatusesQuery,
            uri="/{company}/customer-statuses/",
            method="get"
        )

    def create(self, **data):
        return self.resource(
            model=CustomerStatusesCreateUpdate,
            uri="/{company}/customer-statuses/",
            method="post",
            **data
        )

    def delete(self, customer_status_id):
        return self.resource(
            model=CustomerStatusesQuery,
            uri="/{company}/customer-statuses/{id}/",
            path_param=customer_status_id,
            method="delete"
        )

    def get_by_id(self, customer_status_id):
        return self.resource(
            model=CustomerStatusesQuery,
            uri="/{company}/customer-statuses/{id}/",
            path_param=customer_status_id,
            method="get"
        )

    def patch(self, customer_status_id, **data):
        return self.resource(
            model=CustomerStatusesCreateUpdate,
            uri="/{company}/customer-statuses/{id}/",
            path_param=customer_status_id,
            method="patch",
            **data
        )

    def put(self, customer_status_id, **data):
        return self.resource(
            model=CustomerStatusesCreateUpdate,
            uri="/{company}/customer-statuses/{id}/",
            path_param=customer_status_id,
            method="put",
            **data
        )
