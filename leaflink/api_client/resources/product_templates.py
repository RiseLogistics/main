from .base import API, Model


class ProductTemplatesQuery(Model):
    _QUERY_ = ["page"]


class ProductTemplateVarieties(Model):
    _SCHEMA_ = {
        "unit_of_measure"   : ("int",   Model.OPTIONAL),
        "minimum_order"     : ("int",   Model.OPTIONAL),
        "name"              : ("str",   Model.OPTIONAL),
        "unit_denomination" : ("int",   Model.OPTIONAL),
        "wholesale_price"   : ("int",   Model.OPTIONAL),
        "sale_price"        : ("int",   Model.OPTIONAL),
        "maximum_order"     : ("int",   Model.OPTIONAL),
        "retail_price"      : ("int",   Model.OPTIONAL)
    }


class ProductTemplatesCreateUpdate(Model):
    _SCHEMA_ = {
        "strain_classification" : ("str",   Model.OPTIONAL),
        "description"           : ("str",   Model.OPTIONAL),
        "wholesale_price"       : ("int",   Model.OPTIONAL),
        "template_name"         : ("int",   Model.OPTIONAL),
        "unit_multiplier"       : ("int",   Model.OPTIONAL),
        "SHOW_QUANTITY"         : ("str",   Model.OPTIONAL),
        "category"              : ("str",   Model.OPTIONAL),
        "unit_of_measure"       : ("str",   Model.OPTIONAL),
        "product_data_items"    : ("list",  Model.OPTIONAL),
        "seller"                : ("str",   Model.OPTIONAL),
        "inventory_management"  : ("str",   Model.OPTIONAL),
        "listing_state"         : ("str",   Model.OPTIONAL),
        "sale_price"            : ("int",   Model.OPTIONAL),
        "maximum_order"         : ("int",   Model.OPTIONAL),
        "minimum_order"         : ("int",   Model.OPTIONAL),
        "brand"                 : ("str",   Model.OPTIONAL),
        "AVAILABLE_FOR_SAMPLES" : ("str",   Model.OPTIONAL),
        "retail_price"          : ("int",   Model.OPTIONAL),
        "product_line"          : ("dict",  Model.OPTIONAL),
        "license"               : ("dict",  Model.OPTIONAL),
        "unit_denomination"     : ("str",   Model.OPTIONAL),
        "strains"               : ("list",  Model.OPTIONAL),

        "sell_in_unit_of_measure"    : ("str", Model.OPTIONAL),
        "product_template_varieties" : (ProductTemplateVarieties, Model.OPTIONAL),
    }


class ProductTemplates(API):

    @property
    def list(self):
        return self.resource(
            model=ProductTemplatesQuery,
            uri="/{company}/product-templates/",
            method="get"
        )

    def get_by_id(self, product_template_id):
        return self.resource(
            model=ProductTemplatesQuery,
            uri="/{company}/product-templates/{id}/",
            path_param=product_template_id,
            method="get"
        )

    def patch(self, product_template_id, **data):
        return self.resource(
            model=ProductTemplatesCreateUpdate,
            uri="/{company}/product-templates/{id}/",
            path_param=product_template_id,
            method="patch",
            **data
        )

    def put(self, product_template_id, **data):
        return self.resource(
            model=ProductTemplatesCreateUpdate,
            uri="/{company}/product-templates/{id}/",
            path_param=product_template_id,
            method="put",
            **data
        )

    def delete(self, product_template_id):
        return self.resource(
            model=ProductTemplatesQuery,
            uri="/{company}/product-templates/{id}/",
            path_param=product_template_id,
            method="delete"
        )
