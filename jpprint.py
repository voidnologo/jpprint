import json


def formatter(data, indent):
    try:
        return json.dumps(json.loads(data), indent=indent, sort_keys=True)
    except:
        return json.dumps(data, indent=indent, sort_keys=True)


def max_len(data):
    return max(len(x) for x in data.split('\n'))


def jpprint(f1, f2, indent=4, separator='|', diff_ind='<>'):
    f1 = formatter(f1, indent)
    f2 = formatter(f2, indent)
    l1width = max_len(f1)
    l2width = max_len(f2)
    for l1, l2 in zip(f1.splitlines(), f2.splitlines()):
        delim = diff_ind if l1 != l2 else separator
        print('{:{l1width}}{:^10}{:{l2width}}'.format(l1, delim, l2, l1width=l1width, l2width=l2width))
