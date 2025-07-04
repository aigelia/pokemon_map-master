from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=50, null=False, default='Неизвестный покемон')
    title_en = models.CharField(max_length=50, null=False, blank=True)
    title_jp = models.CharField(max_length=50, null=False, blank=True)
    image = models.ImageField(upload_to='pokemon_images', null=True)
    description = models.TextField(null=False, blank=True)
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
        related_name='entities'
    )
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField(null=True, blank=True)
    disappeared_at = models.DateTimeField(null=True, blank=True)
    level = models.IntegerField(null=True, blank=True)
    health = models.IntegerField(null=True, blank=True)
    strength = models.IntegerField(null=True, blank=True)
    defence = models.IntegerField(null=True, blank=True)
    stamina = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.pokemon}'