# Generated by Django 5.1 on 2024-10-02 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0006_alter_registration_paper_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="registration",
            name="paper_id",
            field=models.CharField(max_length=20, null=True),
        ),
    ]
