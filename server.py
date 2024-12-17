import logging
import os

from blockkit import PlainText
from slack_bolt import App
from slack_sdk.errors import SlackApiError

from services.initiatives.service import get_initiatives
from user_interfaces.create_event import create_modal, process_response
from user_interfaces.create_home import create_home

logging.basicConfig(level=logging.DEBUG)

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
)


@app.middleware  # or app.use(log_request)
def log_request(logger, body, next):
    logger.debug(body)
    next()


# Step 5: Payload is sent to this endpoint, we extract the `trigger_id` and call views.open
@app.command("/thankyou")
def handle_command(body, ack, client, logger):
    logger.info(body)
    ack()

    res = client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "gratitude-modal",
            "title": {"type": "plain_text", "text": "Gratitude Box"},
            "submit": PlainText(text="Submit").build(),
            "close": {"type": "plain_text", "text": "Cancel"},
            "blocks": [
                {
                    "type": "input",
                    "block_id": "my_block",
                    "element": {"type": "plain_text_input", "action_id": "my_action"},
                    "label": {"type": "plain_text", "text": "Say something nice!"},
                }
            ],
        },
    )
    logger.info(res)

@app.action("create_event_button_event")
def button_click(ack, body, client, logger):
    ack()

    res = client.views_open(
        trigger_id=body["trigger_id"],
        view=create_modal(callback_id="simple-modal", initiatives=get_initiatives()).build()
    )
    logger.info(res)


# Step 4: The path that allows for your server to receive information from the modal sent in Slack
@app.view("simple-modal")
def view_submission(ack, body, client, logger):
    # ack()
    # logger.info(body["view"]["state"]["values"])
    # Extra Credit: Uncomment out this section
    # thank_you_channel = "#social"
    # user_text = body["view"]["state"]["values"]["my_block"]["my_action"]["value"]
    client.chat_postMessage(channel=thank_you_channel, text=user_text)
    logger.info("----------RESULT INIT--------")
    event = process_response(body)
    logger.info(event)
    logger.info("----------RESULT FINISH--------")



# Listen to the app_home_opened Events API event to hear when a user opens your app from the sidebar
@app.event("app_home_opened")
def app_home_opened(event, client, logger):
    user_id = event["user"]

    try:
        # Call the views.publish method using the WebClient passed to listeners
        result = client.views_publish(
            user_id=user_id,
            view=create_home(user_id).build()
        )
        logger.info(result)

    except SlackApiError as e:
        logger.error("Error fetching conversations: {}".format(e))


if __name__ == "__main__":
    app.start(3000)
