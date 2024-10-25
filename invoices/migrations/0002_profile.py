# Generated by Django 4.1.4 on 2023-09-11 17:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("invoices", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
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
                ("first_name", models.CharField(blank=True, max_length=200, null=True)),
                ("last_name", models.CharField(blank=True, max_length=200, null=True)),
                ("company", models.CharField(blank=True, max_length=200, null=True)),
                (
                    "email_address",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "mobile_number",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("city", models.CharField(blank=True, max_length=100, null=True)),
                ("country", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "logo",
                    models.ImageField(
                        blank=True, null=True, upload_to="invoicer_companies_logos/"
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
