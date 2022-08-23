""" Migration
"""

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration"""

    initial = True

    dependencies = [
        ("core_parser_app", "0001_initial"),
        ("core_main_app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Curate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
            options={
                "verbose_name": "core_curate_app",
                "permissions": (
                    ("access_curate", "Can access curate"),
                    ("view_data_save_repo", "Can view data save repo"),
                    (
                        "access_curate_data_structure",
                        "Can access curate data structure",
                    ),
                ),
                "default_permissions": (),
            },
        ),
        migrations.CreateModel(
            name="CurateDataStructure",
            fields=[
                (
                    "datastructure_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="core_parser_app.datastructure",
                    ),
                ),
                ("form_string", models.TextField(blank=True)),
                (
                    "data",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core_main_app.data",
                    ),
                ),
            ],
            bases=("core_parser_app.datastructure",),
        ),
    ]
