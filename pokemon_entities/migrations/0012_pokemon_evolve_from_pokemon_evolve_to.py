# Generated by Django 5.2.3 on 2025-07-03 17:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0011_pokemon_title_en_pokemon_title_jp_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='evolve_from',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='next_evolutions', to='pokemon_entities.pokemon', verbose_name='Из кого эволюционирует'),
        ),
        migrations.AddField(
            model_name='pokemon',
            name='evolve_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='previous_evolutions', to='pokemon_entities.pokemon', verbose_name='В кого эволюционирует'),
        ),
    ]
