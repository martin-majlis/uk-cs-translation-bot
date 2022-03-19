import json
import logging
import os
from typing import Any, Dict, Final

import requests
from t_translation import translate

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ENV_TOKEN_NAME = "TELEGRAM_UK_CS_TRANSLATION_BOT_TOKEN"


def respond(err: Any, res: Dict[str, Any] = None):
    body = res if res else err
    return {
        "statusCode": "400" if err else "200",
        "body": json.dumps(body).encode("utf8"),
        "headers": {
            "Content-Type": "application/json",
        },
    }


def lambda_handler(event, _context):
    # check the token
    bot_token: Final = os.environ.get(ENV_TOKEN_NAME)
    if not bot_token:
        logger.error(f"Bot token is not defined; env={ENV_TOKEN_NAME}")
        return respond("Bot token is not defined")

    # extract message text
    if "body" not in event:
        logger.error(f"Incorrect payload; event={event!r}")
        return respond("Body is empty")

    message = json.loads(event["body"]).get("message")
    if not message:
        logger.error(f"Message is is not specified; body={event['body']!r}")
        return respond("Message is missing")

    chat_id = message.get("chat", {}).get("id")
    if not chat_id:
        logger.error(f"Chat is is not specified; message={message!r}")
        return respond("Chat id is missing")

    text = message.get("text")

    # translate message
    out_text = ""
    success = False
    if text:
        translation = translate(text, "telegram")
        if translation.error:
            out_text = translation.error
        else:
            out_text = "\n".join(translation.translation)
            success = True
    else:
        out_text = "Není text / Немає тексту"

    if not success:
        out_text = ":( " + out_text

    r = requests.post(
        f"https://api.telegram.org/bot{bot_token}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": out_text,
        },
        headers={
            "Accept": "application/json",
        },
    )
    if r.status_code != 200:
        logger.error(
            "Message sending has failed; "
            f"status={r.status_code!r}, "
            f"reason={r.reason!r}"
        )

    return respond(None, "OK")
