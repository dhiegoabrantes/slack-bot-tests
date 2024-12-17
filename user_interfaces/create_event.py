from blockkit import Modal, PlainText, Input, PlainTextInput, PlainOption, \
    StaticSelect, Divider, DatetimePicker, MultiStaticSelect

from model.event import Event
from services.deploy_type.deploy_type import DeployType
from services.deploy_type.services import get_deploy_types

# dhiego

INITIATIVES = "initiatives"
INITIATIVES_ACTION = "initiatives-action"
APPLICATIONS = "applications"
APPLICATIONS_ACTION = "applications-action"
DEPLOY_TYPES = "deploy_type"
DEPLOY_TYPES_ACTION = "deploy_type-action"

EVENT_FINISH_DATE_TIME = "event_finish_datetime"
EVENT_FINISH_DATE_TIME_ACTION = "event_finish_datetime-action"
EVENT_START_DATE_TIME = "event_start_date_time"
EVENT_START_DATE_TIME_ACTION = "event_start_date_time-action"


def create_modal(callback_id, initiatives):
    # Defina os blocos de entrada (inputs)
    event_start_datetime = Input(
        block_id=EVENT_START_DATE_TIME,
        label=PlainText(text="Start Event Date", emoji=True),
        element=DatetimePicker(
            action_id=EVENT_START_DATE_TIME_ACTION
        )
    )

    event_finish_datetime = Input(
        block_id=EVENT_FINISH_DATE_TIME,
        label=PlainText(text="Finish Event Date", emoji=True),
        element=DatetimePicker(
            action_id=EVENT_FINISH_DATE_TIME_ACTION
        )
    )

    options = build_initiative_options(initiatives)

    initiatives = Input(
        block_id=INITIATIVES,
        label=PlainText(text="Initiative", emoji=True),
        element=StaticSelect(
            placeholder=PlainText(text="Select the initiative", emoji=True),
            options=options,
            action_id=INITIATIVES_ACTION
        )
    )

    deploy_types = Input(
        block_id=DEPLOY_TYPES,
        label=PlainText(text="Deploy Type", emoji=True),
        element=MultiStaticSelect(
            placeholder=PlainText(text="Select the deploy types", emoji=True),
            options=build_deploy_type_options(get_deploy_types()),
            action_id=DEPLOY_TYPES_ACTION
        )
    )

    applications = Input(
        block_id=APPLICATIONS,
        label=PlainText(text="Applications", emoji=True),
        element=PlainTextInput(action_id=APPLICATIONS_ACTION, placeholder="Impacted applications")
    )

    return Modal(
        title=PlainText(text="Create Event"),
        submit=PlainText(text="Salvar"),
        close=PlainText(text="Cancelar"),
        callback_id=callback_id,
        blocks=[
            event_start_datetime,
            event_finish_datetime,
            Divider(),
            initiatives,
            applications,
            deploy_types
        ]
    )


def build_initiative_options(initiatives):
    initiatives_options = []
    for initiative in initiatives:
        option = PlainOption(text=PlainText(text=initiative.name, emoji=True), value=str(initiative.id))
        initiatives_options.append(option)
    return initiatives_options


def build_deploy_type_options(deploy_types):
    deploy_types_options = []
    for deploy_type in deploy_types:
        option = PlainOption(text=PlainText(text=deploy_type.name, emoji=True), value=str(deploy_type.key))
        deploy_types_options.append(option)
    return deploy_types_options


def process_response(body):
    values = body["view"]["state"]["values"]

    return Event(
        start_datetime=values[EVENT_START_DATE_TIME][EVENT_START_DATE_TIME_ACTION]["selected_date_time"],
        finish_date=values[EVENT_FINISH_DATE_TIME][EVENT_FINISH_DATE_TIME_ACTION]["selected_date_time"],
        initiative=values[INITIATIVES][INITIATIVES_ACTION]["selected_option"]["text"]["text"],
        applications=values[APPLICATIONS][APPLICATIONS_ACTION]["value"],
        deploy_types=process_deploy_type(values[DEPLOY_TYPES][DEPLOY_TYPES_ACTION]["selected_options"])
    )


def process_deploy_type(options):
    deploy_types_options = []
    for option in options:
        deploy_type = DeployType(option["value"], option["text"]["text"])
        deploy_types_options.append(deploy_type)
    return deploy_types_options
