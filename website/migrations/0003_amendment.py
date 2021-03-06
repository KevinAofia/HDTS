# Generated by Django 4.0.3 on 2022-05-09 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_log'),
    ]

    operations = [
        migrations.CreateModel(
            name='Amendment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100)),
                ('amendment_submission_date', models.DateField()),
                ('amendment_decison_date', models.DateField(max_length=254, null=True)),
                ('amendment_description', models.TextField()),
                ('decision_date', models.DateField(max_length=254, null=True)),
                ('comment', models.TextField()),
            ],
        ),
    ]
