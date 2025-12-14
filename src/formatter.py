import datetime
import json
import uuid


def datetime_or_default_handler(*args):
    if isinstance(args[1], (datetime.datetime, datetime.date)):
        return args[1].isoformat()
    if isinstance(args[1], uuid.UUID):
        return str(args[1])
    return f'Unconvertable Type {type(args[1])} - {args[1]}'


json.JSONEncoder.default = datetime_or_default_handler


def formatter(data, indent: int) -> str:
    data = data.decode() if isinstance(data, bytes) else data
    try:
        return json.dumps(json.loads(data), indent=indent, sort_keys=True)
    except Exception:
        return json.dumps(data, indent=indent, sort_keys=True)


def max_len(data: str) -> int:
    return max(len(x) for x in data.split('\n'))


def truncate(data: str, width: int) -> str:
    ellipse = '...'
    return '\n'.join([x[: width - 3] + ellipse if len(x) > width else x for x in data.split('\n')])
