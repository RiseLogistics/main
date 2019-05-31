from .base import API, Model


class CompanyStaffsQuery(Model):
    pass


class CompanyStaffs(API):

    @property
    def list(self):
        return self.resource(
            model=CompanyStaffsQuery,
            uri="/{company}/company-staffs/",
            method="get"
        )

    def get_by_id(self, staff_id):
        return self.resource(
            model=CompanyStaffsQuery,
            uri="/{company}/company-staffs/{id}/",
            path_param=staff_id,
            method="get"
        )
