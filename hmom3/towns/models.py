from django.db import models


class Fractions(models.Model):
    name = models.CharField(max_length=20, verbose_name='Название')
    bonus = models.CharField(max_length=256, verbose_name='Бонус')
    description = models.CharField(max_length=512, verbose_name='Описание')
    image = models.ImageField(
        'Картинка',
        upload_to='fractions/',
        blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Фракция'
        verbose_name_plural = 'Фракции'
