from flask_sqlalchemy import BaseQuery as _BaseQuery
from sqlalchemy import event


class SoftDeletedQuery(_BaseQuery):
    def __init__(self, entities, session=None):
        super().__init__(entities, session=session)
        self.trashed_on = 'not_only_trashed'

    @property
    def only_trashed(self):
        self.trashed_on = 'only_trashed'
        return self

    @property
    def with_trashed(self):
        self.trashed_on = 'with_trashed'
        return self


@event.listens_for(SoftDeletedQuery, 'before_compile', retval=True, bake_ok=True)
def _before_compile(query):
    for desc in query.column_descriptions:
        _model = desc['entity']
        if _model is None:
            continue
        if hasattr(_model, 'deleted_time'):
            if query.trashed_on == 'only_trashed':
                query = query.enable_assertions(False).filter(_model.deleted_time != 0)
            if query.trashed_on == 'not_only_trashed':
                query = query.enable_assertions(False).filter(_model.deleted_time == 0)
    return query

