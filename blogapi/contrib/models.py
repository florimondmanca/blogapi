import orm
from sqlalchemy.sql import text

__all__ = ["QuerySet"]


def prepare_order_args(order_args):
    return [text(arg) for arg in order_args]


class QuerySet(orm.models.QuerySet):
    def __init__(self, order_fields=None, **kwargs):
        super().__init__(**kwargs)
        self._order_fields = order_fields

    def build_select_expression(self):
        expr = super().build_select_expression()

        if self._order_fields is not None:
            order_fields = [text(arg) for arg in self._order_fields]
            expr = expr.order_by(*order_fields)

        return expr

    def order_by(self, *fields):
        if self._order_fields is not None:
            fields = self._order_fields + fields

        return self.__class__(
            model_cls=self.model_cls,
            filter_clauses=self.filter_clauses,
            select_related=self.select_related,
            order_fields=fields,
        )
