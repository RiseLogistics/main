from .base import API, Model


class CustomerTiersQuery(Model):
    _QUERY_ = [
        "limit",
        "offset"
    ]


class CustomerTiers(API):

    @property
    def list(self):
        return self.resource(
            model=CustomerTiersQuery,
            uri="/{company}/customer-tiers/",
            method="get"
        )

    def get_by_id(self, customer_tier_id):
        return self.resource(
            model=CustomerTiersQuery,
            uri="/{company}/customer-tiers/{id}/",
            path_param=customer_tier_id,
            method="get"
        )

