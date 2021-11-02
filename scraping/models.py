from django.db import models
from .utils import from_cyrillic_to_eng


# Create your models here.


class City(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Город')
    slug = models.CharField(max_length=50, blank=True, unique=True, verbose_name='SLUG')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
        super().save(*args, **kwargs)


class Language(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Язык Программирования')
    slug = models.CharField(max_length=50, blank=True, unique=True, verbose_name='SLUG')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Язык Программирования'
        verbose_name_plural = 'Языки Программирования'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
        super().save(*args, **kwargs)


class Vacancy(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=250, verbose_name='Заголовок вакансии')
    company = models.CharField(max_length=250, verbose_name='Компания')
    description = models.TextField(verbose_name='Описание вакансии')
    city = models.ForeignKey('City', on_delete=models.PROTECT, verbose_name='Город')
    language = models.ForeignKey('Language', on_delete=models.PROTECT, verbose_name='Язык программирования')
    timestamp = models.DateField(auto_now_add=True, verbose_name='Дата публикации')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
