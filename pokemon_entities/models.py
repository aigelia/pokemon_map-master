from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(
        max_length=50,
        null=False,
        default='Неизвестный покемон',
        verbose_name='Название покемона'
    )
    title_en = models.CharField(
        max_length=50,
        null=False,
        blank=True,
        verbose_name='Название на английском'
    )
    title_jp = models.CharField(
        max_length=50,
        null=False,
        blank=True,
        verbose_name='Название на японском'
    )
    image = models.ImageField(
        upload_to='pokemon_images',
        null=True,
        verbose_name='Изображение (для отображения на карте и странице покемона)'
    )
    description = models.TextField(
        null=False,
        blank=True,
        verbose_name='Описание'
    )
    previous_evolution = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='next_evolutions',
        on_delete=models.SET_NULL,
        verbose_name="Из кого эволюционирует",
    )

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        related_name='entities',
        verbose_name='Название покемона'
    )
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(null=True, blank=True, verbose_name='Время появления')
    disappeared_at = models.DateTimeField(null=True, blank=True, verbose_name='Время исчезновения')
    level = models.IntegerField(null=True, blank=True, verbose_name='Уровень покемона')
    health = models.IntegerField(null=True, blank=True, verbose_name='Здоровье')
    strength = models.IntegerField(null=True, blank=True, verbose_name='Сила')
    defence = models.IntegerField(null=True, blank=True, verbose_name='Защита')
    stamina = models.IntegerField(null=True, blank=True, verbose_name='Выносливость')

    def __str__(self):
        return f'{self.pokemon}'