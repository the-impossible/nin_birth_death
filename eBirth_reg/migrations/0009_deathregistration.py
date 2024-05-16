# Generated by Django 5.0.6 on 2024-05-15 12:48

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("eBirth_reg", "0008_rename_pic_hospitalprofile_signature"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="DeathRegistration",
            fields=[
                (
                    "death_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("date_of_death", models.DateField()),
                ("age_at_death", models.CharField(max_length=3)),
                ("place_of_death", models.CharField(max_length=100)),
                ("address_of_deceased", models.CharField(max_length=100)),
                ("certificate_num", models.CharField(max_length=10)),
                ("date_issue", models.DateTimeField(auto_now_add=True)),
                (
                    "hospital_issued",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="eBirth_reg.hospitalprofile",
                    ),
                ),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Death Registrations",
                "db_table": "Death Registration",
            },
        ),
    ]
