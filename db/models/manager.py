from __future__ import absolute_import

import logging

from django.db.models.manager import Manager, QuerySet
from django.utils import timezone

__all__ = ("BaseManager",)

logger = logging.getLogger("")


class BaseQuerySet(QuerySet):
    def update(self, *args, **kwargs):
        super().update(*args, **kwargs, updated_at=timezone.now())


class BaseManager(Manager):

    _queryset_class = BaseQuerySet

    def __init__(self, *args, **kwargs):
        super(BaseManager, self).__init__(*args, **kwargs)

    def post_save(self, instance, **kwargs):
        """
        Triggered when a model bound to this manager is saved.
        """

    def post_delete(self, instance, **kwargs):
        """
        Triggered when a model bound to this manager is deleted.
        """

    def get_queryset(self):
        """
        Returns a new QuerySet object.  Subclasses can override this method to
        easily customize the behavior of the Manager.
        """
        if hasattr(self, "_hints"):
            return self._queryset_class(
                self.model, using=self._db, hints=self._hints
            )
        return self._queryset_class(self.model, using=self._db)
