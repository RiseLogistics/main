from .base import API, Model
from .discussions import DiscussionsQuery


class DiscussionMessages(API):

    @property
    def list(self):
        return self.resource(
            model=DiscussionsQuery,
            uri="/{company}/discussion-messages/",
            method="get"
        )

    def get_by_id(self, discussion_id):
        return self.resource(
            model=DiscussionsQuery,
            uri="/{company}/discussion-messages/{id}/",
            path_param=discussion_id,
            method="get"
        )
