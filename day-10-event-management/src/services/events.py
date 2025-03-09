from models.events import events
from random import choices
def create_new_event(payload):
    choices_list ="abcdefhjdjdjkdj12334447883893773-_"
    event_id = "".join(choices(choices_list,k=12))
    event = {**payload,"id":event_id}
    events.append(event)
    return event