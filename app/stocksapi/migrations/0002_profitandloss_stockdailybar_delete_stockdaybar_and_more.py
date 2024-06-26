# Generated by Django 4.2.3 on 2024-05-19 18:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stocksapi", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProfitAndLoss",
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
                ("date", models.DateField(blank=True, null=True)),
                ("min_change", models.FloatField()),
                ("max_change", models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name="StockDailyBar",
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
                ("ticker", models.CharField(max_length=12)),
                ("timestamp", models.DateTimeField(blank=True, null=True)),
                ("open_price", models.FloatField()),
                ("close_price", models.FloatField()),
                ("highest_price", models.FloatField()),
                ("lowest_price", models.FloatField()),
            ],
        ),
        migrations.DeleteModel(
            name="StockDayBar",
        ),
        migrations.AddField(
            model_name="profitandloss",
            name="last_bar",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="last_bar",
                to="stocksapi.stockdailybar",
            ),
        ),
        migrations.AddField(
            model_name="profitandloss",
            name="stock_bar",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="stock_bar",
                to="stocksapi.stockdailybar",
            ),
        ),
    ]
