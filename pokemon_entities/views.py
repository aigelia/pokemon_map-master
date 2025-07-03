import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import localtime, now

from pokemon_entities.models import PokemonEntity, Pokemon

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    current_time = localtime(now())
    pokemon_entities = PokemonEntity.objects.filter(
        appeared_at__lte=current_time,
        disappeared_at__gte=current_time
    )

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for entity in pokemon_entities:
        add_pokemon(
            folium_map,
            entity.lat,
            entity.lon,
            request.build_absolute_uri(entity.pokemon.image.url) if entity.pokemon.image else DEFAULT_IMAGE_URL
        )

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.image.url if pokemon.image else '',
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    requested_pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    current_time = localtime(now())
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for entity in PokemonEntity.objects.filter(
        pokemon=requested_pokemon,
        appeared_at__lte=current_time,
        disappeared_at__gte=current_time
    ):
        add_pokemon(
            folium_map, entity.lat,
            entity.lon,
            request.build_absolute_uri(entity.pokemon.image.url) if entity.pokemon.image else DEFAULT_IMAGE_URL
        )

    pokemon_on_page = {
        'pokemon_id': requested_pokemon.id,
        'img_url': request.build_absolute_uri(requested_pokemon.image.url) if requested_pokemon.image else DEFAULT_IMAGE_URL,
        'title_ru': requested_pokemon.title,
        'title_en': requested_pokemon.title_en,
        'title_jp': requested_pokemon.title_jp,
        'description': requested_pokemon.description,
    }

    if requested_pokemon.previous_evolution:
        evolve_from = requested_pokemon.previous_evolution
        pokemon_on_page['previous_evolution'] = {
            'pokemon_id': evolve_from.id,
            'title_ru': evolve_from.title,
            'img_url': request.build_absolute_uri(evolve_from.image.url) if evolve_from.image else DEFAULT_IMAGE_URL,
        }

    next_evolutions = requested_pokemon.next_evolutions.all()
    if next_evolutions.exists():
        evolve_to = next_evolutions.first()  # например, берем первую следующую эволюцию, если их несколько
        pokemon_on_page['next_evolution'] = {
            'pokemon_id': evolve_to.id,
            'title_ru': evolve_to.title,
            'img_url': request.build_absolute_uri(evolve_to.image.url) if evolve_to.image else DEFAULT_IMAGE_URL,
        }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(),
        'pokemon': pokemon_on_page,
    })
