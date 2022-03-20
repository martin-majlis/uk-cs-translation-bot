import json
import logging
import os
from typing import Any, Dict, Final

import requests
from v_translation import translate

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ENV_TOKEN_NAME = "VIBER_UK_CS_TRANSLATION_BOT_TOKEN"


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

    body = json.loads(event["body"])

    event_type = body.get("event")
    if not event_type:
        logger.error(f"Event type is is not specified; body={body!r}")
        return respond("Event type is missing")

    if event_type != "message":
        logger.info(f"Unsupported event type; event_type={event_type}")
        return respond(None, "Unsupported event type")

    sender_id = body.get("sender", {}).get("id")
    if not sender_id:
        logger.error(f"Sender is is not specified; message={body!r}")
        return respond("Sender id is missing")

    # message_type = body.get("message", {}).get("type")
    text = body.get("message", {}).get("text")

    # translate message
    out_text = ""
    success = False
    if text:
        translation = translate(text, "viber")
        if translation.error:
            out_text = translation.error
        else:
            out_text = "\n".join(translation.translation)
            success = True
    else:
        out_text = "Není text / Немає тексту"

    if not success:
        out_text = ":( " + out_text

    # https://developers.viber.com/docs/api/rest-bot-api/#send-message
    r = requests.post(
        "https://chatapi.viber.com/pa/send_message",
        json={
            "receiver": sender_id,
            "sender": {
                "name": "UkCsTranslationBot",
            },
            "type": "text",
            "text": out_text,
        },
        headers={
            "Accept": "application/json",
            "X-Viber-Auth-Token": bot_token,
        },
    )
    if r.status_code != 200:
        logger.error(
            "Message sending has failed; "
            f"status={r.status_code!r}, "
            f"reason={r.reason!r}"
        )

    return respond(None, "OK")
