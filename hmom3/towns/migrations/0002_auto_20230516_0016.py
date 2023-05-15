# Generated by Django 2.2.16 on 2023-05-15 18:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('towns', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbuilding',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buildings', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='resource',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='resource', to=settings.AUTH_USER_MODEL, verbose_name='Ресурсы'),
        ),
        migrations.AddField(
            model_name='buildingrequirement',
            name='building',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='towns.Building', verbose_name='Здание'),
        ),
        migrations.AddField(
            model_name='buildingrequirement',
            name='requirement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='requirements', to='towns.Building', verbose_name='Требование'),
        ),
        migrations.AddField(
            model_name='buildinginprocess',
            name='building',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='towns.UserBuilding', verbose_name='Строения'),
        ),
        migrations.AddField(
            model_name='buildinginprocess',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='buildings2', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='building',
            name='fraction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='towns.Fraction', verbose_name='Фракция'),
        ),
        migrations.AddField(
            model_name='building',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='types', to='towns.BuildingType', verbose_name='Тип'),
        ),
        migrations.AddConstraint(
            model_name='userbuilding',
            constraint=models.UniqueConstraint(fields=('user', 'building'), name='unique_user_building'),
        ),
        migrations.AddConstraint(
            model_name='building',
            constraint=models.UniqueConstraint(fields=('type', 'fraction'), name='unique_type_fraction'),
        ),
    ]