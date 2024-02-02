import os
from unittest import skipIf

from django.conf import settings
from django.test import TestCase

from app.models import Customer, CustomerWithRandomID
from govtech_csg_xcg.securemodelpkid import (
    DEFAULT_ID_INT_DIGITS,
    DEFAULT_ID_TEXT_LENGTH,
    MIN_ID_TEXT_LENGTH,
)


class TestRandomIDGenerationUsingRandomIDModel(TestCase):
    """Tests for random ID generation where the model inherits from
    govtech_csg_xcg.securemodelpkid.model.RandomIDModel.
    """

    def setUp(self):
        specified_id_text_length = getattr(settings, "ID_TEXT_LENGTH", None)
        if specified_id_text_length is None:
            self.correct_id_text_length = DEFAULT_ID_TEXT_LENGTH
        elif specified_id_text_length < MIN_ID_TEXT_LENGTH:
            self.correct_id_text_length = MIN_ID_TEXT_LENGTH
        else:
            self.correct_id_text_length = specified_id_text_length

    def test_generate_random_string_ids(self):
        customer = CustomerWithRandomID(name="test")
        customer.save()

        self.assertTrue(isinstance(customer.id, str))
        self.assertEqual(len(customer.id), self.correct_id_text_length)
        print(f"Random ID string: {customer.id}")

    def test_generate_random_string_ids_during_data_migration(self):
        # This customer would already have been created during data migration.
        # See tests/app/migrations/0002_data_migrations.py
        # The purpose of this is to prevent a regression for the issue where
        # RandomIDModel's custom 'save' method is inaccessible during a data migration.
        customer = CustomerWithRandomID.objects.get(name="0002_data_migration")
        self.assertTrue(isinstance(customer.id, str))
        self.assertEqual(len(customer.id), self.correct_id_text_length)
        print(f"Random ID string: {customer.id}")


SETTINGS_WITHOUT_APP_INSTALLED = [
    "core.settings_without_app",
    "core.settings_without_app_min_length",
]


# We skip these tests if the settings file does not install the securemodelpkid app
# as these tests depend on the app being installed.
@skipIf(
    os.getenv("DJANGO_SETTINGS_MODULE") in SETTINGS_WITHOUT_APP_INSTALLED,
    reason="App not installed.",
)
class TestRandomIDGenerationUsingApp(TestCase):
    """Tests for random ID generation using the installed apps method.

    This should affect all models that inherit from django.db.models.Model.
    """

    def test_generate_random_integer_ids(self):
        customer = Customer(name="test")
        customer.save()

        self.assertTrue(isinstance(customer.id, int))
        self.assertEqual(len(str(customer.id)), DEFAULT_ID_INT_DIGITS)
        print(f"Random ID integer: {customer.id}")

    def test_generate_random_integer_ids_during_data_migration(self):
        # This customer would already have been created during data migration.
        # See tests/app/migrations/0002_data_migrations.py
        # The purpose of this is to prevent a regression for the issue where
        # RandomIDModel's custom 'save' method is inaccessible during a data migration.
        # Although the issue shouldn't apply to models using the 'app method', we add
        # this test to make sure that this does not change.
        customer = Customer.objects.get(name="0002_data_migration")
        self.assertTrue(isinstance(customer.id, int))
        self.assertEqual(len(str(customer.id)), DEFAULT_ID_INT_DIGITS)
        print(f"Random ID integer: {customer.id}")
