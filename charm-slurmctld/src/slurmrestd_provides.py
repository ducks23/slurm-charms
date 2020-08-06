#!/usr/bin/python3
"""SlurmrestdProvides."""
import json
import logging


from ops.framework import Object


logger = logging.getLogger()


class SlurmrestdProvides(Object):
    """Slurmrestd Provides Relation."""

    def __init__(self, charm, relation_name):
        """Set the initial data."""
        super().__init__(charm, relation_name)
        self.charm = charm
        self.framework.observe(
            charm.on[relation_name].relation_created,
            self._on_relation_created
        )

    def _on_relation_created(self, event):
        slurmdbd_acquired = self.charm.is_slurmdbd_available()
        slurmd_acquired = self.charm.is_slurmd_available()
        slurm_installed = self.charm.is_slurm_installed()
        if not (slurmdbd_acquired and slurmd_acquired and slurm_installed):
            event.defer()
            return
        else:
            event.relation.data[self.model.unit]["slurm_config"] = json.dumps(
                self.charm.get_slurm_config()
            )
            self.charm.set_slurmrestd_available(True)
