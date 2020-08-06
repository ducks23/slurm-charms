#!/usr/bin/python3
"""SlurmrestdProvides."""
import logging


from ops.framework import (
    EventBase,
    EventSource,
    Object,
    ObjectEvents,
)


logger = logging.getLogger()


class SlurmrestdAvailableEvent(EventBase):
    """Emmited when slurmrestd is available."""


class SlurmrestdUnAvailableEvent(EventBase):
    """Emmited when the slurmrestd relation is broken."""


class SlurmrestdProvidesEvents(ObjectEvents):
    """SlurmrestdProvidesEvents."""

    slurmrestd_available = EventSource(SlurmrestdAvailableEvent)
    slurmrestd_unavailable = EventSource(SlurmrestdUnAvailableEvent)


class SlurmrestdProvides(Object):
    """Slurmrestd Provides Relation."""

    on = SlurmrestdProvidesEvents()

    def __init__(self, charm, relation_name):
        """Set the initial data."""
        super().__init__(charm, relation_name)

        self.charm = charm
        self.framework.observe(
            charm.on[relation_name].relation_created,
            self._on_relation_created
        )

    def _on_relation_created(self, event):
        self.charm.set_slurmrestd_available(True)
        self.on.slurmrestd_available.emit()

    def _on_relation_broken(self, event):
        self.charm.set_slurmrestd_available(False)
        self.on.slurmrestd_unavailable.emit()
