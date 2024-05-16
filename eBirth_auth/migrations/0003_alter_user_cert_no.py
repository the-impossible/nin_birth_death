# Generated by Django 4.1.7 on 2023-03-27 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("eBirth_auth", "0002_user_is_hospital_admin"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="cert_no",
            field=models.CharField(
                blank=True, db_index=True, max_length=10, null=True, unique=True
            ),
        ),
    ]