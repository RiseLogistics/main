from .base import API, Model


class PaymentTermsQuery(Model):
    _QUERY_ = [
        "limit",
        "offset"
    ]


class PaymentTerms(API):

    @property
    def list(self):
        return self.resource(
            model=PaymentTermsQuery,
            uri="/{company}/payment-terms/",
            method="get"
        )

    def get_by_id(self, payment_terms_id):
        return self.resource(
            model=PaymentTermsQuery,
            uri="/{company}/payment-terms/{id}/",
            path_param=payment_terms_id,
            method="get"
        )
