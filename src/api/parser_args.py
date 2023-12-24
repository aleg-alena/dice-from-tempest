from aiogram.types import Message


def parse_args(message: Message, *args: callable) -> list:
    message_args = message.text.split()[1:]

    if len(message_args) != len(args):
        raise IndexError

    try:
        return [validator(arg) for validator, arg in zip(args, message_args)]
    except Exception:
        raise ValueError
