# Generated by Django 5.1.2 on 2024-10-09 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OcrAws',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='whatis/img')),
                ('text', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
