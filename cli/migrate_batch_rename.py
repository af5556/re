import json
import click
import copy
import pathlib


def migrate_conf(conf):
    new_conf = copy.deepcopy(conf)
    new_conf.pop("change")
    new_conf["change"] = []
    changes = conf["change"]
    key_map = {}
    for change in changes:
        if change["transform"]["function"] == "rename_key":
            key_map[change["transform"]["arguments"]["old"]] = change["transform"]["arguments"]["new"]
        else:
            new_conf["change"].append(change)
    if len(key_map.keys()):
        new_conf["change"].append({
                "v_type": "dict",
                "transform": {
                    "function": "rename_key",
                    "arguments": {
                        "rename_map": key_map,
                        "keep_other_keys": False
                    },
                },
            }
        )
    return new_conf


def migrate_input(conf):
    for table in conf["input"]:
        if "pre_transform" in table.keys():
            table["pre_transform"] = migrate_conf(table["pre_transform"])
    return conf


@click.command()
@click.option('--jfile')
def migrate(jfile):
    new_conf = {}
    with open(jfile, "r") as _:
        conf = json.load(_)
    if "change" in conf.keys():
        new_conf = migrate_conf(conf)
    elif "input" in conf.keys():
        new_conf = migrate_input(conf)
    with open(f"output_{pathlib.Path(jfile).name}", "w") as _:
        json.dump(new_conf, _, indent=2)


if __name__ == "__main__":
    migrate()
