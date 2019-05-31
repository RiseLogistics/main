from .base import API, Model


class ActivityQuery(Model):
    _QUERY_ = [
        "limit",
        "offset",
        "author",
        "customer",
        "staff",
        "type",
        "brand",
        "ordering",
        "search"
    ]

class ActivityEntries(API):

    @property
    def list(self):
        return self.resource(
            model=ActivityQuery,
            method="get",
            uri="/{company}/activity-entries/"
        )

    def get_by_id(self, activity_entries_id):
        return self.resource(
            model=ActivityQuery,
            method="get",
            uri="/{company}/activity-entries/{id}/",
            path_param=activity_entries_id
        )

    @property
    def deleted(self):
        return self.resource(
            model=ActivityQuery,
            method="get",
            uri="/{company}/activity-entries/deleted/"
        )


