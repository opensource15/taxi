# Generated by Django 5.0.4 on 2024-05-30 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='student_id_card',
            field=models.ImageField(blank=True, null=True, upload_to='student_id_cards/'),
        ),
    ]
