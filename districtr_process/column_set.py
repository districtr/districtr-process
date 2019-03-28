class ColumnSet:
    """A set of related columns. E.g. a population or election data."""

    def __init__(self, total=None, subgroups=None, metadata=None):
        self.total = total
        if subgroups is None:
            subgroups = []
        self.subgroups = subgroups
        if metadata is None:
            metadata = dict()
        self.metadata = metadata

    def __repr__(self):
        subgroups_string = ", ".join(subgroup.key for subgroup in subgroups)
        return "<{} [{}]>".format(self.__class__.__name__, subgroups_string)

    @property
    def columns(self):
        if self.total is None:
            return self.subgroups
        return [self.total] + self.subgroups

    def record(self, df=None):
        result = {}
        if self.total is not None:
            result["total"] = summarize_column(self.total, df)

        result["subgroups"] = [
            summarize_column(subgroup, df) for subgroup in self.subgroups
        ]

        if len(self.metadata) > 0:
            result["metadata"] = self.metadata

        return result


def summarize_column(column, df=None):
    if df is not None:
        return {
            "key": column.key,
            "name": column.name,
            "sum": int(df[column.key].sum()),
            "min": int(df[column.key].min()),
            "max": int(df[column.key].max()),
        }
    else:
        return {"key": column.key, "name": column.name}
