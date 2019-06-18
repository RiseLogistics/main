from .base import API, Model


class OrdersQuery(Model):
    _QUERY_ = [
        "limit",
        "offset",
        "status",
        "number",
        "buyer",
        "seller",
        "user",
        "buyer__name",
        "user__email",
        "user__first_name",
        "user__last_name",
        "ordering",
        "search"
    ]


class OrdersUpdate(Model):
    _SCHEMA_ = {
        "shipping_charge"       :   ("int",  Model.OPTIONAL),
        "delivery_preferences"  :   ("str",  Model.OPTIONAL),
        "tax_amount"            :   ("int",  Model.OPTIONAL),
        "shipping_details"      :   ("str",  Model.OPTIONAL),
        "payment_term"          :   ("str",  Model.OPTIONAL),
        "external_id_seller"    :   ("str",  Model.OPTIONAL),
        "tax_type"              :   ("str",  Model.OPTIONAL),
        "internal_notes"        :   ("str",  Model.OPTIONAL),
        "manual"                :   ("bool", Model.OPTIONAL),
        "paid"                  :   ("bool", Model.OPTIONAL),
        "ship_date"             :   ("str",  Model.OPTIONAL),
        "discount_type"         :   ("str",  Model.OPTIONAL),
        "external_id_buyer"     :   ("str",  Model.OPTIONAL),
        "paid_date"             :   ("str",  Model.OPTIONAL),
        "payment_due_date"      :   ("str",  Model.OPTIONAL),
        "total"                 :   ("int",  Model.OPTIONAL),
        "notes"                 :   ("str",  Model.OPTIONAL),
        "status"                :   ("str",  Model.OPTIONAL),
        "discount_amount"       :   ("int",  Model.OPTIONAL)
    }

    _QUERY_ = OrdersQuery._QUERY_


class Orders(API):

    @property
    def list(self):
        return self.resource(
            model=OrdersQuery,
            uri="/{company}/orders/",
            method="get"
        )

    def delete(self, order_number):
        return self.resource(
            model=OrdersQuery,
            uri="/{company}/orders/{id}/",
            path_param=order_number,
            method="delete"
        )

    def get_by_number(self, order_number):
        return self.resource(
            model=OrdersQuery,
            uri="/{company}/orders/{id}/",
            path_param=order_number,
            method="get"
        )

    def patch(self, order_number, **data):
        return self.resource(
            model=OrdersUpdate,
            uri="/v2/orders-received/{id}/",
            path_param=order_number,
            method="patch",
            **data
        )

    def patch(self, order_number, **data):
        return self.resource(
            model=OrdersUpdate,
            uri="/v2/orders-received/{id}/",
            path_param=order_number,
            method="patch",
            **data
        )

    def rpc_status(self, order_number, status, **data):
        return self.resource(
            model=OrdersUpdate,
            uri="/v2/orders-received/{id}/transition/%s" % status,
            path_param=order_number,
            method="post",
            **data
        )

    def put(self, order_number, **data):
        return self.resource(
            model=OrdersUpdate,
            uri="/{company}/orders/{id}/",
            path_param=order_number,
            method="put",
            **data
        )

