import json
import logging
import os
from typing import Any, Dict, Final

import requests
from m_translation import translate

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ENV_VERIFY_TOKEN_NAME = "MESSENGER_UK_CS_TRANSLATION_BOT_VERIFY_TOKEN"
ENV_PAGE_ACCESS_TOKEN = "MESSENGER_UK_CS_TRANSLATION_BOT_PAGE_ACCESS_TOKEN"


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
    logger.info(event)

    # Verification part
    # https://developers.facebook.com/docs/messenger-platform/webhook#setup
    qs = event.get("queryStringParameters")  # type: Dict[str, str]
    if qs:
        expected_token: Final = os.environ.get(ENV_VERIFY_TOKEN_NAME)
        if not expected_token:
            logger.error(f"Verify token is not defined; env={ENV_VERIFY_TOKEN_NAME}")
            return respond("Verify token is not defined")

        challenge = qs.get("hub.challenge")
        mode = qs.get("hub.mode")
        verify_token = qs.get("hub.verify_token")
        if mode and verify_token:
            if mode == "subscribe" and verify_token == expected_token:
                return {
                    "statusCode": "200",
                    "body": challenge,
                }
            else:
                logger.error(
                    f"Unknown mode or token; mode={mode}; token={verify_token}"
                )
                return respond("Unknown mode or token")
        else:
            logger.error(f"Unknown query string; qs={qs!r}")
            return respond("Unknown query string")

    # extract message text
    if "body" not in event:
        logger.error(f"Incorrect payload; event={event!r}")
        return respond("Body is empty")

    entry = json.loads(event["body"]).get("entry")
    if not entry:
        logger.error(f"Entry is is not specified; body={event['body']!r}")
        return respond("Entry is missing")

    if len(entry) > 1:
        logger.warning(f"More than one entry; entry={entry!r}")

    messaging = entry[0].get("messaging")
    if not messaging:
        logger.error(f"Messaging is not specified; messaging={entry[0]!r}")
        return respond("Messaging is missing")

    if len(messaging) > 1:
        logger.warning(f"More than one messaging; messaging={messaging!r}")

    # https://developers.facebook.com/docs/messenger-platform/reference/webhook-events/messages
    inp_message = messaging[0]
    sender_id = inp_message.get("sender", {}).get("id")
    # recipient_id = inp_message.get("recipient", {}).get("id")
    # message_id = inp_message.get("message", {}).get("mid")
    text = inp_message.get("message", {}).get("text")

    access_token: Final = os.environ.get(ENV_PAGE_ACCESS_TOKEN)
    if not access_token:
        logger.error(f"Access token is not defined; env={ENV_PAGE_ACCESS_TOKEN}")
        return respond("Access token is not defined")

    # translate message
    out_text = ""
    success = False
    if text:
        translation = translate(text, "messenger")
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
        f"https://graph.facebook.com/v13.0/me/messages?access_token={access_token}",
        json={
            "messaging_type": "RESPONSE",
            "recipient": {"id": sender_id},
            "message": {
                "text": out_text,
            },
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
