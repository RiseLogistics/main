from .base import API, Model


class ProductLineQuery(Model):
    _QUERY_ = ["page"]


class ProductLine(API):

    @property
    def list(self):
        return self.resource(
            model=ProductLineQuery,
            uri="/{company}/product-lines/",
            method="get"
        )

    def get_by_id(self, product_line_id):
        return self.resource(
            model=ProductLineQuery,
            uri="/{company}/product-lines/{id}/",
            path_param=product_line_id,
            method="get"
        )

