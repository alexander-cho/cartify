# Generated by Django 5.0.3 on 2024-03-26 19:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"verbose_name_plural": "categories"},
        ),
        migrations.AlterField(
            model_name="product",
            name="name",
            field=models.CharField(max_length=100),
        ),
    ]
