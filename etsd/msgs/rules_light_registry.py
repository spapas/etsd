import rules_light


def can_read(user, _rule, msg) -> bool:
    authority = user.get_authority()
    return len([x for x in msg.participant_set.all() if x.authority == authority]) > 0


# This function is used to use the prefetch related participant_set
def participant_is_participant(msg, user):
    authority = user.get_authority()
    return (
        len(
            [
                x
                for x in msg.participant_set.all()
                if x.authority == authority and x.kind == "SENDER"
            ]
        )
        > 0
    )


def can_add_data(user, _rule, msg) -> bool:
    return msg.status == "DRAFT" and participant_is_participant(msg, user)


def can_send(user, _rule, msg) -> bool:
    if msg.data_set.all().count() == 0:
        return False  # no data to send
    return msg.status == "DRAFT" and participant_is_participant(msg, user)


# This function uses the prefetch related participant_set
def get_auth_participant(msg, user):
    return [
        x for x in msg.participant_set.all() if x.authority == user.get_authority()
    ][0]


def can_archive(user, _rule, msg) -> bool:
    if msg.status == "DRAFT":
        return False

    participant = get_auth_participant(msg, user)
    return participant.status == "READ"


def can_unarchive(user, _rule, msg) -> bool:
    if msg.status == "DRAFT":
        return False

    participant = get_auth_participant(msg, user)
    return participant.status == "ARCHIVED"


rules_light.registry["msgs.message.read"] = can_read
rules_light.registry["msgs.message.add_data"] = can_add_data
rules_light.registry["msgs.message.send"] = can_send
rules_light.registry["msgs.message.delete"] = can_add_data
rules_light.registry["msgs.message.archive"] = can_archive
rules_light.registry["msgs.message.unarchive"] = can_unarchive


def can_delete_cipherdata(user, rule, cipher_data) -> bool:
    message = cipher_data.data.message
    if can_add_data(user, rule, message):
        return True
    # if the message is not draft, we can delete the cipher data *only* if we have read the message
    participant = get_auth_participant(message, user)
    return participant.status == "READ"


rules_light.registry["msgs.cipherdata.delete"] = can_delete_cipherdata
