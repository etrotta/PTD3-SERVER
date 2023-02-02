from urllib.parse import quote, unquote
from io import BytesIO

from main import app

path = '/public'
test_bodies = [
    # (
    #     'Action=createAccount',
    # ),
    # (
    #     'Action=loadAccount',
    # ),
    # (
    #     'Action=saveStory',
    #     'whichProfile=2',
    #     # 'extra=Save=true&NewGameSave=true&Nickname=Etrotta&Color=2&Gender=0&CS=null&MSave=true&MA=ym&LevelSave=true&LevelA=y&LevelC=y&PokeNick1=Pichu&PokeNick2=Rattata',
    #     # It actually should be encoded here
    #     'extra=Save%3Dtrue%26NewGameSave%3Dtrue%26Nickname%3DEtrotta%26Color%3D2%26Gender%3D0%26CS%3Dnull%26MSave%3Dtrue%26MA%3Dym%26LevelSave%3Dtrue%26LevelA%3Dy%26LevelC%3Dy%26PokeNick1%3DPichu%26PokeNick2%3DRattata',
    #     'extra2=yeyyyyyy',
    #     'extra3=woeywyyyymyycyrwycyyrypwwwcqapycymyyyyymymymynyyymymymyyyymyywyoywyeyqyyycyqymyyyyyyymymynycymymym',
    #     'extra4=yeyyywyy',
    #     'extra5=pymw',
    # ),
    # (
    #     'Action=loadStory',
    # ),
    (
        'Action=loadStoryProfile',
        'whichProfile=1',
    ),
]

test_bodies = [
    '&'.join(
        (
            *body,
            # 'Public' server. The Pass is just to interact with the server, not with deta itself, 
            # and I do not mind people having access to that game account.
            f'Email={quote(f"https://ptd3server-3-o2189185.deta.app{path}")}',
            'Pass=JgpTobfD5y3SCrjLEW1sGGhSFvX8gAod',
            )
        )
    .encode('UTF-8')
    for body in test_bodies
]

def get_environ(path: str, body: bytes) -> dict:
    environ = {
        "CONTENT_LENGTH": str(len(body)),
        "PATH_INFO": path,
        "REMOTE_ADDR": "127.0.0.1",
        "wsgi.input": BytesIO(body),
    }
    return environ

for body in test_bodies:
    print(app(get_environ(path, body), print))
