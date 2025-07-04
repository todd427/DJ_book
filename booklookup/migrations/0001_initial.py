# Generated by Django 5.2.3 on 2025-06-23 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('authors', models.CharField(max_length=300)),
                ('isbn_10', models.CharField(blank=True, max_length=20, null=True)),
                ('isbn_13', models.CharField(blank=True, max_length=20, null=True)),
                ('asin', models.CharField(blank=True, max_length=20, null=True)),
                ('source', models.CharField(max_length=100)),
                ('price', models.CharField(blank=True, max_length=20, null=True)),
                ('purchase_url', models.URLField(blank=True, null=True)),
            ],
        ),
    ]
