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
from django.conf import settings
from django.db import models

from . import DEFAULT_ID_TEXT_LENGTH, MIN_ID_TEXT_LENGTH
from .helpers import generate_random_id

try:
    ID_TEXT_LENGTH = settings.ID_TEXT_LENGTH
    if ID_TEXT_LENGTH < MIN_ID_TEXT_LENGTH:
        ID_TEXT_LENGTH = MIN_ID_TEXT_LENGTH
except Exception:
    ID_TEXT_LENGTH = DEFAULT_ID_TEXT_LENGTH


class RandomIDModel(models.Model):
    """Provides a model base that transparently generates a random string with
    IDLENGTH length as its primary key, which is robust to collisions.
    """

    class Meta:
        abstract = True

    id = models.CharField(max_length=ID_TEXT_LENGTH, primary_key=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_random_id(self.__class__, type="str")
        super().save(*args, **kwargs)

    @classmethod
    def get_effective_id_length(cls):
        return ID_TEXT_LENGTH
