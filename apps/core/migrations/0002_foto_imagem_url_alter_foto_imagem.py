# Generated by Django 5.2.1 on 2025-05-20 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='foto',
            name='imagem_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='foto',
            name='imagem',
            field=models.ImageField(blank=True, null=True, upload_to='fotos/'),
        ),
    ]
