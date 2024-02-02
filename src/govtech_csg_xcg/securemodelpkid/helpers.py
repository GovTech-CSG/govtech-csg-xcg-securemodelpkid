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
import secrets
import string

from django.db.models import Model as DjangoModelBase

from . import DEFAULT_ID_INT_DIGITS


def generate_random_id(model: DjangoModelBase, type: str = "str"):
    """Generates a collision-free random ID for a model class."""
    if not issubclass(model, DjangoModelBase):
        raise TypeError(
            "First argument passed to generate_random_id must be a Django model class."
        )

    if type not in ("str", "int"):
        raise ValueError('Value of "type" must be either "str" or "int".')

    generate, length = None, None
    # The ideal method would be to check if 'model' is a subclass of
    # RandomIDModel. Unfortunately, specific class information is lost
    # during Django data migrations, because Django creates a 'fake'
    # of the model classes so as to prevent use of custom model methods.
    from .model import RandomIDModel

    if type == "str":
        length = RandomIDModel.get_effective_id_length()
        generate = lambda len: secrets.token_urlsafe(len)[:len]  # noqa: E731
    else:
        length = DEFAULT_ID_INT_DIGITS
        generate = lambda len: int(  # noqa: E731
            secrets.choice(string.digits[1:])
            + "".join(secrets.choice(string.digits) for i in range(len - 1))
        )

    is_unique = False
    while not is_unique:
        candidate = generate(length)
        is_unique = not model.objects.filter(id=candidate).exists()
    return candidate
