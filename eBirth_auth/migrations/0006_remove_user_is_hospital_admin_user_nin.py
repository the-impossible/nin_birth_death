# Generated by Django 5.0.6 on 2024-05-14 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("eBirth_auth", "0005_alter_user_pic"),
    ]

    operations = [
        migrations.RemoveField(model_name="user", name="is_hospital_admin",),
        migrations.AddField(
            model_name="user",
            name="nin",
            field=models.CharField(
                blank=True, db_index=True, max_length=10, null=True, unique=True
            ),
        ),
    ]
