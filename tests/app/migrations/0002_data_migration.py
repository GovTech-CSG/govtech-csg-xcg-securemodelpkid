from django.db import migrations

from govtech_csg_xcg.securemodelpkid.helpers import generate_random_id


def create_records(apps, schema_editor):
    """Create some records as part of a data migration."""
    Customer = apps.get_model("app", "Customer")
    Customer(name="0002_data_migration").save()

    CustomerWithRandomID = apps.get_model("app", "CustomerWithRandomID")
    CustomerWithRandomID(
        id=generate_random_id(CustomerWithRandomID), name="0002_data_migration"
    ).save()


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [migrations.RunPython(create_records)]
