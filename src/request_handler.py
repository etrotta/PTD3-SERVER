import random

from models.networking import Request, Response
from models.extractor import encode
from manage_save import get_profiles_list, get_story_profile, set_save_data

CS = encode("12345")

def get_UID():
    # Used in-game to determine one thing (`get_Trainer_Specific_Elemental` function)
    return str(random.randint(100, 1000))

def create_check_sum(data: str) -> int:
    "Creates a checksum"
    return sum(ord(x) - 96 for x in data.lower()) * 3 + 45


def handle_request(request: Request):
    # print(request)
    action = request.data.get("Action")
    if action == "createAccount":  # From: screen.screen_Main @ Register
        return Response(Result='Success', UID=get_UID(), Reason='loadedAccount')
    elif action == "loadAccount":  # From: screen.screen_Main @ Login
        return Response(Result='Success', UID=get_UID(), Reason='loadedAccount')
    elif action == "loadStory":  # From: screen.popup_StoryLoad
        data = get_profiles_list(request)
        return Response(Result='Success', **data)
    elif action == "loadStoryProfile":  # From: screen.popup_Story_Profile_Load
        data = get_story_profile(request)
        _check_sum = encode(str(create_check_sum(data['extra3'] + CS)))
        return Response(Result='Success', **data, CS=CS, extra5=_check_sum)
    elif action == "saveStory":  # From: scren.popup_Story_Save
        data = set_save_data(request)
        return Response(Result='Success', CS=CS, **data)
    elif "deleteStory":  # From: scren.popup_Story_Delete
        raise NotImplementedError('oops')
        return Response(Result='', Reason='')
    else:
        raise Exception(f"Unexpected action: {request.data.get('Action')}", request)
