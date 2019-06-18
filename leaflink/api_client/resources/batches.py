from .base import API, Model


class ProductBatchesQuery(Model):
    _QUERY_ = [
        "limit",
        "offset"
    ]


class ProductUpdateCreate(Model):
    _SCHEMA_ = {
        "owner": ("str", Model.OPTIONAL),
        "production_batch_number": ("str", Model.OPTIONAL),
        "batch_date" : ("str", Model.OPTIONAL),
    }


class ProductBatches(API):
    @property
    def list(self):
        return self.resource(
            model=ProductBatchesQuery,
            uri="/v2/batches/",
            method="get"
        )

    def create(self, **data):
        return self.resource(
            model=ProductUpdateCreate,
            uri="/v2/batches/",
            method="post",
            **data
        )

    def delete(self, company_contact_id):
        return self.resource(
            model=ProductBatchesQuery,
            uri="/v2/batches/{id}/",
            path_param=company_contact_id,
            method="delete"
        )

    def get_by_id(self, company_contact_id):
        return self.resource(
            model=ProductBatchesQuery,
            uri="/v2/batches/{id}/",
            path_param=company_contact_id,
            method="get"
        )

    def patch(self, company_contact_id, **data):
        return self.resource(
            model=ProductUpdateCreate,
            uri="/v2/batches/{id}/",
            path_param=company_contact_id,
            method="patch",
            **data
        )

    def put(self, company_contact_id, **data):
        return self.resource(
            model=ProductUpdateCreate,
            uri="/v2/batches/{id}/",
            path_param=company_contact_id,
            method="put",
            **data
        )


class AssociateBatchesQuery(Model):
    _QUERY_ = [
        "limit",
        "offset"
    ]


class AssociateBatchesCreate(Model):
    _SCHEMA_ = {
        "product": ("str", Model.OPTIONAL),
        "batch": ("in", Model.OPTIONAL),
    }


class AssociateBatches(API):
    @property
    def list(self):
        return self.resource(
            model=ProductBatchesQuery,
            uri="/v2/product-batches/",
            method="get"
        )

    def associate(self, **data):
        return self.resource(
            model=ProductUpdateCreate,
            uri="/v2/product-batches/",
            method="post",
            **data
        )
