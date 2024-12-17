from blockkit import PlainText, Home, Section, MarkdownText, Image, Actions, Button
from pydantic.networks import HttpUrl

def create_home(user_id):
    return Home(
        blocks=[
            Section(
                text=MarkdownText(text="Welcome to User Accounts Bot, <@{}>!".format(user_id)),
                accessory=Image(
                    image_url=HttpUrl("https://api.slack.com/img/blocks/bkb_template_images/notifications.png"),
                    alt_text="Calendar Thumbnail"
                )
            ),
            Actions(elements=[
                Button(
                    text=PlainText(text="Create Event"),
                    value="create_event_button",
                    action_id="create_event_button_event",
                )
            ])
        ]
    )

def teste():
    return "oi!"