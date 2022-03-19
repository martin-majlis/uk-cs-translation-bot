# Diary

## 2022-03-19

- Create Telegram Bot
  - Looks super easy - https://core.telegram.org/bots
    - With few clicks I have http://t.me/uk_cs_translation_bot
  - Create Lambda Function
  - Set up webhook
    - ```
      curl -X GET "https://api.telegram.org/bot${TELEGRAM_UK_CS_TRANSLATION_BOT_TOKEN}/getMe"
      ```
    - ```
      curl -X POST "https://api.telegram.org/bot${TELEGRAM_UK_CS_TRANSLATION_BOT_TOKEN}/setWebhook" \
      -H "Content-Type: application/json" \
      -d "{'url': '${TELEGRAM_UK_CS_TRANSLATION_BOT_LAMBDA}'}"
      ```
    - ```
      curl -X GET "https://api.telegram.org/bot${TELEGRAM_UK_CS_TRANSLATION_BOT_TOKEN}/getWebhookInfo"
      ```
  - Build package
    - https://docs.aws.amazon.com/lambda/latest/dg/python-package.html#python-package-prereqs
  - Initial version is up and running - http://t.me/uk_cs_translation_bot
- Create WhatsApp Bot
- Create Messenger Bot
  - https://developers.facebook.com/docs/messenger-platform/
  - After few clicks there is:
    - https://fb.me/uk.cs.translation.bot
    - https://m.me/uk.cs.translation.bot
  - API:
    - https://developers.facebook.com/docs/messenger-platform/webhook
    - https://developers.facebook.com/docs/messenger-platform/reference/webhook-events/messages
  - Waiting for approval
