import os
import json
from pprint import pprint


mapper_types = {
    str: lambda x, y: cast_string(x, default=y),
    None: lambda x, y: cast_null(x),
    int: lambda x, y: cast_integers(x, default=y),
    float: lambda x, y: cast_numbers(x, default=y),
    dict: lambda x, y: cast_dict(x),
    list: lambda x, y: cast_list(x),
    bool: lambda x, y: cast_bool(x, default=y)
}


def cast_bool(value, default=False):
    return value or default


def cast_null(value):
    return value or None


def cast_list(value):
    return value or []


def cast_dict(value):
    return value or {}


def cast_string(value, default=''):
    return value or default


def cast_numbers(value, default=0):
    return float(value or default)


def cast_integers(value, default=0):
    return int(value or default)


def check_json(d, schema):
    for k, v in d.items():
        if isinstance(v, dict):
            check_json(v, schema[k])
        elif isinstance(v, list):
            for list_i in v:
                check_json(list_i, schema[k][0])
        else:
            schema_return = schema[k]
            func_check = mapper_types[type(schema_return)]
            d[k] = func_check(d[k], schema_return)


if __name__ == '__main__':
    json_schema = None
    with open("structure.json", "r") as json_file:
        json_schema = json.loads(json_file.read())

    with open("data.json", "r") as json_file:
        json_load = json.loads(json_file.read())
        check_json(json_load, json_schema)
        pprint(json_load)
