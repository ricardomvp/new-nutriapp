# Generated by Django 3.1.3 on 2020-11-11 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('card_id', models.TextField(blank=True, null=True)),
                ('card_url', models.TextField(blank=True, null=True)),
                ('card_response', models.TextField(blank=True, null=True)),
                ('dangerousness', models.IntegerField(blank=True, null=True)),
                ('display', models.BooleanField(default=True)),
            ],
        ),
    ]