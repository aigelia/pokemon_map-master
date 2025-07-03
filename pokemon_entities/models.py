from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=50, null=True)
    title_en = models.CharField(max_length=50, null=True)
    title_jp = models.CharField(max_length=50, null=True)
    image = models.ImageField(upload_to='pokemon_images', null=True, blank=True)
    description = models.TextField(null=True)

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField(null=True)
    disappeared_at = models.DateTimeField(null=True, blank=True)
    level = models.IntegerField(default=0)
    health = models.IntegerField(default=0)
    strength = models.IntegerField(default=0)
    defence = models.IntegerField(default=0)
    stamina = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.pokemon}'