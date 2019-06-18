from .base import API, Model
from random import randint


class CustomerCreateUpdate(Model):
    _SCHEMA_ = {
        "business_license_name" : ("str", Model.OPTIONAL),
        "business_identifier"   : ("str", Model.OPTIONAL),
        "license_number"        : ("str", Model.OPTIONAL),
        "delivery_preferences"  : ("str", Model.OPTIONAL),
        "price_schedule"        : ("dict", Model.OPTIONAL),
        "shipping_charge"       : ("int", Model.OPTIONAL),
        "next_contact_date"     : ("str", Model.OPTIONAL),

        "website"       : ("str",   Model.OPTIONAL),
        "managers"      : ("list",  Model.OPTIONAL),
        "payment_term"  : ("dict",  Model.OPTIONAL),
        "dba"           : ("str",   Model.OPTIONAL),
        "service_zone"  : ("dict",  Model.OPTIONAL),
        "county"        : ("dict",  Model.OPTIONAL),
        "partner"       : ("str",   Model.OPTIONAL),
        "city"          : ("str",   Model.OPTIONAL),
        "archived"      : ("bool",  Model.OPTIONAL),
        "delinquent"    : ("bool",  Model.OPTIONAL),
        "zipcode"       : ("str",   Model.OPTIONAL),
        "unit_number"   : ("str",   Model.OPTIONAL),
        "status"        : ("dict",  Model.OPTIONAL),
        "description"   : ("str",   Model.OPTIONAL),
        "tags"          : ("list",  Model.OPTIONAL),
        "phone"         : ("str",   Model.OPTIONAL),
        "address"       : ("str",   Model.OPTIONAL),
        "tier"          : ("dict",  Model.OPTIONAL),
        "nickname"      : ("str",   Model.OPTIONAL),
        "name"          : ("str",   Model.OPTIONAL),
        "notes"         : ("str",   Model.OPTIONAL),
        "email"         : ("str",   Model.OPTIONAL),
        "license_type"  : ("dict",  Model.OPTIONAL),
        "external_id"   : ("int",   Model.OPTIONAL),
        "ein"           : ("str",   Model.OPTIONAL)
    }


class CustomersQuery(Model):
    _QUERY_ = [
        "business_license_name",
        "partner__name",
        "limit",
        "offset",
        "tier",
        "nickname",
        "external_id",
        "license_number",
        "license_type",
        "license_type__type",
        "ein",
        "payment_term",
        "status",
        "name",
        "dba",
        "business_license_name",
        "city",
        "state",
        "delinquent",
        "tags",
        "zipcode",
        "license",
        "license_types",
        "partner",
        "sales_rep",
        "service_zone",
        "archived",
        "search",
        "ordering"
    ]



class Customers(API):

    @property
    def list(self):
        return self.resource(
            model=CustomersQuery,
            uri="/v1/{company}/customers/",
            method="get"
        )

    def create(self, **data):
        return self.resource(
            model=CustomerCreateUpdate,
            uri="/v1/{company}/customers/",
            method="post",
            **data
        )

    @property
    def archived(self):
        return self.resource(
            model=CustomersQuery,
            uri="/v1/{company}/customers/archived/",
            method="get"
        )

    def delete(self, customer_id):

        # patch the sku with a rand num.
        # deleting a customer on leaflink archives it, rather
        # than removing it from the DB. This will cause conflicts
        # if a previously used used IDs value needs to be assigned
        # to another Customer!
        try:
            _r = lambda : str(randint(1000000, 9000000))
            _id = _r() + "-DELETED-CUSTOMER-" + _r()
            self.patch(
                customer_id,
                name=_id,
                address=_id,
                external_id=_id,
                city=_id,
                state=_id,
                dba=_id,
                nickname=_id
            ).run()
        except: pass

        return self.resource(
            model=CustomersQuery,
            uri="/v1/{company}/customers/{id}/",
            path_param=customer_id,
            method="delete"
        )

    def get_by_id(self, customer_id):
        return self.resource(
            model=CustomersQuery,
            uri="/v1/{company}/customers/{id}/",
            path_param=customer_id,
            method="get"
        )

    def patch(self, customer_id, **data):
        return self.resource(
            model=CustomerCreateUpdate,
            uri="/v1/{company}/customers/{id}/",
            path_param=customer_id,
            method="patch",
            **data
        )

    def put(self, customer_id, **data):
        return self.resource(
            model=CustomerCreateUpdate,
            uri="/v1/{company}/customers/{id}/",
            path_param=customer_id,
            method="put",
            **data
        )

    def activities(self, customer_id):
        return self.resource(
            model=CustomersQuery,
            uri="/v1/{company}/customers/{id}/activities/",
            path_param=customer_id,
            method="get"
        )

    def contacts(self, customer_id):
        return self.resource(
            model=CustomersQuery,
            uri="/v1/{company}/customers/{id}/contacts/",
            path_param=customer_id,
            method="get"
        )


