# Generated by Django 5.0.3 on 2024-05-30 23:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("payment", "0004_order_is_shipped"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="date_shipped",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]