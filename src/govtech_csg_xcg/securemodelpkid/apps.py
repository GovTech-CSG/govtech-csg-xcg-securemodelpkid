# ------------------------------------------------------------------------
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# This file incorporates work covered by the following copyright:
#
# Copyright (c) 2024 Agency for Science, Technology and Research (A*STAR).
#   All rights reserved.
# Copyright (c) 2024 Government Technology Agency (GovTech).
#   All rights reserved.
# ------------------------------------------------------------------------
from django.apps import AppConfig
from django.db import models

from .helpers import generate_random_id


class AcasAppConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "govtech_csg_xcg.securemodelpkid"

    def ready(self):
        models.Model.orig_save = models.Model.save

        # Override the Model.save method to add some custom behavior
        def save_override(self, *args, **kwargs):
            pk = None
            for field in self._meta.get_fields():
                if field.primary_key:
                    pk = field
                    break

            if (
                isinstance(pk, models.BigAutoField)
                and hasattr(self, "id")
                and not self.id
            ):
                # do some custom behavior before saving
                self.id = generate_random_id(self.__class__, type="int")

            models.Model.orig_save(self, *args, **kwargs)

        # Modify the Model class to use the overridden save method
        models.Model.save = save_override
