import rules_light


def can_read(user, _rule, msg) -> bool:
    authority = user.get_authority()
    return msg.participant_set.filter(authority=authority).exists()


def can_add_data(user, _rule, msg) -> bool:
    authority = user.get_authority()
    return (
        msg.status == "DRAFT"
        and msg.participant_set.filter(authority=authority, kind="SENDER").exists()
    )


def can_send(user, _rule, msg) -> bool:
    authority = user.get_authority()
    if msg.data_set.all().count() == 0:
        return False  # no data to send
    return (
        msg.status == "DRAFT"
        and msg.participant_set.filter(authority=authority, kind="SENDER").exists()
    )


def can_archive(user, _rule, msg) -> bool:
    if msg.status == "DRAFT":
        return False

    participant = msg.participant_set.get(authority=user.get_authority())
    return participant.status == "READ"


def can_unarchive(user, _rule, msg) -> bool:
    if msg.status == "DRAFT":
        return False

    participant = msg.participant_set.get(authority=user.get_authority())
    return participant.status == "ARCHIVED"


rules_light.registry["msgs.message.read"] = can_read
rules_light.registry["msgs.message.add_data"] = can_add_data
rules_light.registry["msgs.message.send"] = can_send
rules_light.registry["msgs.message.delete"] = can_add_data
rules_light.registry["msgs.message.archive"] = can_archive
rules_light.registry["msgs.message.unarchive"] = can_unarchive
