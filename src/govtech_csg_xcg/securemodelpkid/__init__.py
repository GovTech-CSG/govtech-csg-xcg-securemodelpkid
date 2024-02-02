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
import django

# Handle older versions of Django.
if django.VERSION < (3, 2):
    default_app_config = "govtech_csg_xcg.securemodelpkid.apps.AcasAppConfig"

# Define some constants for ID length.
MIN_ID_TEXT_LENGTH = 18
DEFAULT_ID_TEXT_LENGTH = 32
DEFAULT_ID_INT_DIGITS = 18
