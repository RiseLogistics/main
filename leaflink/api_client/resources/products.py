import random

from .base import API, Model


class ProductsQuery(Model):
    _QUERY_ = [
        "limit",
        "offset",
        "name",
        "sku",
        "listing_state",
        "inventory_management",
        "brand",
        "product_line",
        "type",
        "category",
        "strain_classification",
        "license",
        "ordering",
        "search"
    ]


class ProductsCreateUpdate(Model):
    _SCHEMA_ = {
        "wholesale_price"           : ("str",   Model.OPTIONAL),
        "extern_acct_id"            : ("str",   Model.OPTIONAL),
        "extern_income_acct_id"     : ("str",   Model.OPTIONAL),
        "featured"                  : ("str",   Model.OPTIONAL),
        "cost"                      : ("int",   Model.OPTIONAL),
        "unit_multiplier"           : ("int",   Model.OPTIONAL),
        "images"                    : ("list",  Model.OPTIONAL),
        "children"                  : ("list",  Model.OPTIONAL),
        "sku"                       : ("str",   Model.OPTIONAL),
        "strain_classification"     : ("str",   Model.OPTIONAL),
        "unit_of_measure"           : ("int",   Model.OPTIONAL),
        "unit_denomination"         : ("str",   Model.OPTIONAL),
        "tagline"                   : ("str",   Model.OPTIONAL),
        "inventory_management"      : ("str",   Model.OPTIONAL),
        "listing_state"             : ("str",   Model.OPTIONAL),
        "sale_price"                : ("int",   Model.OPTIONAL),
        "maximum_order"             : ("int",   Model.OPTIONAL),
        "drop_date"                 : ("str",   Model.OPTIONAL),
        "category"                  : ("str",   Model.OPTIONAL),
        "minimum_order"             : ("str",   Model.OPTIONAL),
        "description"               : ("str",   Model.OPTIONAL),
        "brand"                     : ("str",   Model.OPTIONAL),
        "AVAILABLE_FOR_SAMPLES"     : ("bool",  Model.OPTIONAL),
        "retail_price"              : ("int",   Model.OPTIONAL),
        "product_line"              : ("dict",  Model.OPTIONAL),
        "name"                      : ("str",   Model.OPTIONAL),
        "license"                   : ("dict",  Model.OPTIONAL),
        "product_data_items"        : ("list",  Model.OPTIONAL),
        "is_medical_line_item"      : ("bool",  Model.OPTIONAL),
        "strains"                     : ("list",  Model.OPTIONAL),
        "sell_in_unit_of_measure"     : ("str",   Model.OPTIONAL),
        "quantity"                    : ("int",   Model.OPTIONAL),
        "allow_fractional_quantities" : ("int", Model.OPTIONAL),
        "manufacturer"                : ("int", Model.OPTIONAL),
        "seller"                      : ("int", Model.OPTIONAL),
    }


class Products(API):

    @property
    def list(self):
        return self.resource(
            model=ProductsQuery,
            uri="/v2/products/",
            method="get"
        )

    def get_by_id(self, product_id):
        return self.resource(
            model=ProductsQuery,
            uri="/v2/products/{id}/",
            path_param=product_id,
            method="get"
        )

    def create(self, **data):
        return self.resource(
            model=ProductsCreateUpdate,
            uri="/v2/products/",
            method="post",
            **data
        )

    def patch(self, product_id, **data):
        return self.resource(
            model=ProductsCreateUpdate,
            uri="/v2/products/{id}/",
            path_param=product_id,
            method="patch",
            **data
        )

    def put(self, product_id, **data):
        return self.resource(
            model=ProductsCreateUpdate,
            uri="/v2/products/{id}/",
            path_param=product_id,
            method="put",
            **data
        )

    def delete(self, product_id):
        # patch the sku with a rand num.
        # deleting a product on leaflink archives it, rather
        # than removing it from the DB. This will cause conflicts
        # if a previously used used SKU value needs to be assigned
        # to another product!
        
        # Note: this behaviour carried over from v1
        
        try:
            _r = lambda : str(random.randint(1000000, 9000000))
            _sku = _r() + "-DELETED-PRODUCT-" + _r()
            self.patch(product_id, sku=_sku).run()
        except: pass

        return self.resource(
            model=ProductsQuery,
            uri="/v2/products/{id}/",
            path_param=product_id,
            method="delete"
        )


class ProductImages(API):

    def list(self, product_id):
        return self.resource(
            model=ProductsQuery,
            uri="/v2/products/{id}/images/",
            path_param=product_id,
            method="get"
        )

    def get_by_id(self, product_id, image_id):
        _uri = "/v2/products/{id}/image/" + str(image_id)

        return self.resource(
            model=ProductsQuery,
            uri=_uri,
            path_param=product_id,
            method="get"
        )

    def create(self, product_id, **data):
        return self.resource(
            model=ProductsCreateUpdate,
            uri="/v2/products/{id}/image/",
            path_param=product_id,
            method="post",
            **data
        )

    def put(self, product_id, image_id, **data):
        _uri = "/v2/products/{id}/image/" + str(image_id)

        return self.resource(
            model=ProductsCreateUpdate,
            uri=_uri,
            path_param=product_id,
            method="put",
            **data
        )

    def delete(self, product_id, image_id):
        _uri = "/v2/products/{id}/image/" + str(image_id)

        return self.resource(
            model=ProductsQuery,
            uri=_uri,
            path_param=product_id,
            method="delete"
        )

