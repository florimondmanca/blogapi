def equal_dicts(d1: dict, d2: dict, ignore: tuple = ()) -> bool:
    d1_filtered = dict((k, v) for k, v in d1.items() if k not in ignore)
    d2_filtered = dict((k, v) for k, v in d2.items() if k not in ignore)
    return d1_filtered == d2_filtered
