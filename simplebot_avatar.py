import io
import random
import string
from urllib.parse import quote_plus

import requests
import simplebot
from simplebot.bot import Replies

__version__ = "1.0.0"
HEADERS = {
    "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0)"
    " Gecko/20100101 Firefox/60.0"
}


@simplebot.command
def avatar_cat(payload: str, replies: Replies) -> None:
    """Generate a cat avatar based on the given text.

    If no text is given a random avatar is generated.
    """
    replies.add(**_get_reply(payload, "2016_cat-generator"))


@simplebot.command
def avatar_bird(payload: str, replies: Replies) -> None:
    """Generate a bird avatar based on the given text.

    If no text is given a random avatar is generated.
    """
    replies.add(**_get_reply(payload, "2019_bird-generator"))


def _get_reply(text: str, generator: str) -> dict:
    url = "https://www.peppercarrot.com/extras/html/{}/".format(generator)
    if not text:
        text = _generate_token(13)
    url += "avatar.php?seed=" + quote_plus(text)
    with requests.get(url, headers=HEADERS) as resp:
        resp.raise_for_status()
        return dict(text=text, filename="avatar.png", bytefile=io.BytesIO(resp.content))


def _generate_token(length: int) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


class TestPlugin:
    def test_avatar_cat(self, mocker):
        msg = mocker.get_one_reply("/avatar_cat")
        assert msg.is_image()

        msg = mocker.get_one_reply("/avatar_cat test avatar")
        assert msg.is_image()

    def test_avatar_bird(self, mocker):
        msg = mocker.get_one_reply("/avatar_bird")
        assert msg.is_image()

        msg = mocker.get_one_reply("/avatar_bird test avatar")
        assert msg.is_image()
