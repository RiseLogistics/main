from .base import API, Model

class DiscussionsQuery(Model):
    _QUERY_ = []


class Discussions(API):

    @property
    def list(self):
        return self.resource(
            model=DiscussionsQuery,
            uri="/{company}/discussions/",
            method="get"
        )

    def get_by_id(self, discussion_id):
        return self.resource(
            model=DiscussionsQuery,
            uri="/{company}/discussions/{id}/",
            path_param=discussion_id,
            method="get"
        )


