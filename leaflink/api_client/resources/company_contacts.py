from .base import API, Model


class CompanyContactsQuery(Model):
    _QUERY_ = [
        "limit",
        "offset",
        "first_name",
        "last_name",
        "email",
        "customers",
        "secondary_email",
        "role",
        "phone",
        "secondary_phone",
        "ordering",
        "search"
    ]


class CompanyContactsUpdateCreate(Model):
    _SCHEMA_ = {
        "company_customers" : ("list",  Model.OPTIONAL),
        "first_name"        : ("str",   Model.OPTIONAL),
        "last_name"         : ("str",   Model.OPTIONAL),
        "description"       : ("str",   Model.OPTIONAL),
        "secondary_email"   : ("str",   Model.OPTIONAL),
        "phone"             : ("str",   Model.OPTIONAL),
        "role"              : ("str",   Model.OPTIONAL),
        "secondary_phone"   : ("str",   Model.OPTIONAL),
        "email"             : ("str",   Model.OPTIONAL)
    }


class CompanyContacts(API):

    @property
    def list(self):
        return self.resource(
            model=CompanyContactsQuery,
            uri="/{company}/contacts/",
            method="get"
        )

    def create(self, **data):
        return self.resource(
            model=CompanyContactsUpdateCreate,
            uri="/{company}/contacts/",
            method="post",
            **data
        )

    @property
    def deleted(self):
        return self.resource(
            model=CompanyContactsQuery,
            uri="/{company}/contacts/deleted/",
            method="get"
        )

    def delete(self, company_contact_id):
        return self.resource(
            model=CompanyContactsQuery,
            uri="/{company}/contacts/{id}/",
            path_param=company_contact_id,
            method="delete"
        )

    def get_by_id(self, company_contact_id):
        return self.resource(
            model=CompanyContactsQuery,
            uri="/{company}/contacts/{id}/",
            path_param=company_contact_id,
            method="get"
        )

    def patch(self, company_contact_id, **data):
        return self.resource(
            model=CompanyContactsUpdateCreate,
            uri="/{company}/contacts/{id}/",
            path_param=company_contact_id,
            method="patch",
            **data
        )

    def put(self, company_contact_id, **data):
        return self.resource(
            model=CompanyContactsUpdateCreate,
            uri="/{company}/contacts/{id}/",
            path_param=company_contact_id,
            method="put",
            **data
        )
