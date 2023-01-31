from urllib.parse import unquote

from .models.networking import Request

from .models.extras_2 import ExtraInfoLoader, ExtraInfo
from .models.pokemon import PokeLoader, Pokemon
from .models.items import ItemsLoader, Item
from .models.profile import ProfileLoader, Profile

from .models.extractor import encode, decode

from src.database import Database, Query, Field


profile_base = Database("ptd3_profiles_database", record_type=Profile)

extra_base = Database("ptd3_extra_info_database", record_type=ExtraInfo)
poke_base = Database("ptd3_pokemon_database", record_type=Pokemon)
item_base = Database("ptd3_item_database", record_type=Item)


def get_profiles_list(request: Request) -> dict:
    result = {}
    mail = request.data['Email']
    profiles: list[Profile] = profile_base.fetch(Query(Field("key").startswith(mail + '$')))
    data = ProfileLoader.encode_profiles(profiles, result)
    result['extra'] = data
    return result

def get_story_profile(request: Request) -> dict:
    profile_key = f"{request.data['Email']}${request.data['whichProfile']}"
    profile = profile_base.get(profile_key)
    extras = extra_base.fetch()
    pokemons = poke_base.fetch(follow_last=True)
    items = item_base.fetch()
    result = dict()
    result['extra'] = ProfileLoader.encode_story_profile(profile, result)
    result['extra2'] = ExtraInfoLoader.encode_story_extras(extras, result)
    result['extra3'] = PokeLoader.encode_story_pokemons(pokemons, result)
    result['extra4'] = ItemsLoader.encode_story_items(items, result)
    # extra5 and CS are added by the caller
    return result


def set_save_data(request: Request) -> dict:
    "Saves the data and returns the new pokemons IDs"
    profile_meta = {
        outer_key: part
        for outer_key, part in (x.split('=') for x in unquote(request.data["extra"]).split('&'))
    }
    profile_key = f"{request.data['Email']}${request.data['whichProfile']}"

    profile = profile_base.get(profile_key)
    saved_pokemons = poke_base.fetch(follow_last=True)
    profile: Profile = ProfileLoader.update_profile(profile, profile_meta)
    profile.profile_id = request.data['whichProfile']  # not part of the proper `extra` metadata

    _poke_nicks = {int(key.removeprefix('PokeNick')): value for key, value in profile_meta.items() if key.startswith('PokeNick')}

    extras = ExtraInfoLoader(data=request.data['extra2'], infos=[])
    pokemons = PokeLoader(data=request.data['extra3'], pokemons=saved_pokemons, poke_nicks=_poke_nicks)
    items = ItemsLoader(data=request.data['extra4'], items=[])
    # extra5 => current save key ; only used for the checkSum, which we ignore

    extras.load()
    pokemons.load()
    items.load()

    profile_base[profile_key] = profile
    extra_base.put_many(extras.infos, key_source='info_id')
    
    poke_base.put_many(pokemons.to_insert + pokemons.to_update, key_source='poke_save_id', iter=True)
    for poke in pokemons.to_delete:
        poke_base.delete(poke.poke_save_id)
    
    item_base.put_many(items.items, key_source='item_id')

    result = {}
    for pokemon in pokemons.to_insert:
        result[f'PID{pokemon.poke_party_pos}'] = pokemon.poke_save_id
    return result
