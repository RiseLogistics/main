from .base import API, Model

""""
****** NOTE ******

/create Returns a 500!

TODO: Contact LeafLink for support if this endpoint is needed in the future.
******************
"""


class CustomerContactsQuery(Model):
    _QUERY_ = [
        "limit",
        "offset",
        "ordering",
        "search"
    ]


class CustomerContactsCreateUpdate(Model):
    _SCHEMA_ = {
        "is_primary" : ("bool", Model.REQUIRED)
    }


class CustomerContacts(API):

    @property
    def list(self):
        return self.resource(
            model=CustomerContactsQuery,
            uri="/{company}/customer-contacts/",
            method="get"
        )

    def create(self, **data):
        return self.resource(
            model=CustomerContactsCreateUpdate,
            uri="/{company}/customer-contacts/",
            method="post",
            **data
        )

    def delete(self, customer_contact_id):
        return self.resource(
            model=CustomerContactsQuery,
            uri="/api/{company}/customer-contacts/{id}/",
            path_param=customer_contact_id,
            method="delete"
        )

    def get_by_id(self, customer_contact_id):
        return self.resource(
            model=CustomerContactsQuery,
            uri="/api/{company}/customer-contacts/{id}/",
            path_param=customer_contact_id,
            method="get"
        )

    def patch(self, customer_contact_id, **data):
        return self.resource(
            model=CustomerContactsCreateUpdate,
            uri="/api/{company}/customer-contacts/{id}/",
            path_param=customer_contact_id,
            method="patch",
            **data
        )

    def put(self, customer_contact_id, **data):
        return self.resource(
            model=CustomerContactsCreateUpdate,
            uri="/api/{company}/customer-contacts/{id}/",
            path_param=customer_contact_id,
            method="put",
            **data
        )

