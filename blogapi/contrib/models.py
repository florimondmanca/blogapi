import typing
import orm

__all__ = ["QuerySet"]


def prepare_order(model, order: typing.List[str]) -> typing.List[str]:
    prepared = []

    for clause in order:
        try:
            col_name, operation = clause.split(" ")
        except ValueError:
            col_name = clause
            desc = False
        else:
            assert operation == "desc"
            desc = True

        col = model.__table__.columns[col_name]
        prepared.append(col.desc() if desc else col)

    return prepared


class QuerySet(orm.models.QuerySet):
    def __init__(
        self, order: typing.Optional[typing.List[str]] = None, **kwargs
    ):
        super().__init__(**kwargs)
        self._order = order

    def build_select_expression(self):
        expr = super().build_select_expression()

        if self._order is not None:
            order = prepare_order(self.model_cls, self._order)
            expr = expr.order_by(*order)

        return expr

    def order_by(self, *order):
        if self._order is not None:
            order = self._order + order

        return self.__class__(
            model_cls=self.model_cls,
            filter_clauses=self.filter_clauses,
            select_related=self._select_related,
            order=order,
        )


orm.models.FILTER_OPERATORS.update({"is": "is_", "isnot": "isnot"})
