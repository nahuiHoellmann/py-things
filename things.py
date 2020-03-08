import subprocess
import urllib.parse
import json
from datetime import date


def __build_url(data):
    url = "".join([
        'things:///json?data=',
        urllib.parse.quote_plus(json.dumps(data, separators=(',', ':')))
    ])
    url = url.replace("+", "%20")
    return url


def add_items(data):
    url = __build_url(data)
    subprocess.call(["open", url])


# TODO: Implement
# def add_project(title, **kwargs):
#     """summary
#     Build a things api compliant task out of the provided arguments
#     Parameters
#     ----------
#     title: str
#     notes: str, optional
#     when: date, optional
#     deadline: date, optional
#     tags: list, optional
#     area_id: str, optional
#     area: str, optional
#     completed: bool, optional
#         Defaut False
#     canceled: bool, optional
#         Default False
#     """
#     pass

def create_checklist_item(source):
    if isinstance(source, str):
        return {
            "type": "checklist-item",
            "attributes": {
                "title": source
            }
        }
    elif isinstance(source, tuple):
        title, completed = source
        if isinstance(title, str) and isinstance(completed, bool):
            return {
                "type": "checklist-item",
                "attributes": {
                    "title": title,
                    "completed": completed
                }
            }
    raise TypeError(f"In checklist_items: expected str or (str, bool) but got {type(source)} instead")  # noqa: E501


def __typecheck_create_task(title, **kwargs):

    if not isinstance(title, str):
        raise TypeError(f"title: expected str but got {type(title)}")

    optionals = {
        "notes": str,
        "when": date,
        "deadline": date,
        "tags": list,
        "checklist_items": list,
        "project_id": str,
        "project_name": str,
        "heading": str,
        "completed": bool,
        "canceled": bool
    }

    for k, v in kwargs.items():
        if k not in optionals:
            raise TypeError(f'Got unexepected keyword argument {k}')
        provided_type = type(v)
        expected_type = optionals[k]
        if expected_type is not provided_type:
            raise TypeError(f"{k}: expected {expected_type} but got {provided_type}")  # noqa: E501


def create_task(title, **kwargs):
    """summary
    Build a things api compliant task out of the provided arguments
    Parameters
    ----------
    title: str
    notes: str, optional
    when: date, optional
    deadline: date, optional
    tags: list, optional
    checklist_items: List[str | (str, bool)], optional
        str is the title and bool is wheter the item has been completed
        if only a str is provided bool is asumed to be false
    project_id: str, optional
    project_name: str, optional
    heading: str, optional
    completed: bool, optional
        Default False
    canceled: bool, optional
        Default False
    """
    __typecheck_create_task(title, **kwargs)

    if kwargs.get('checklist_items'):
        kwargs['checklist-items'] = []
        for item in kwargs['checklist_items']:
            checklist_item = create_checklist_item(item)
            kwargs['checklist-items'].append(checklist_item)
        del kwargs['checklist_items']

    # Some keys must be corrected due to the grammar differences in python and json  # noqa: E501
    if kwargs.get("project_id"):
        kwargs["list-id"] = kwargs.pop("project_id")

    if kwargs.get("project_name"):
        kwargs["list"] = kwargs.pop("project_name")

    return {
        "type": "to-do",
        "attributes": {
            "title": title,
            **kwargs
        }
    }


def add_task(title, **kwargs):
    """"summary

    Parameters
    ----------
    title: str
    notes: str, optional
    when: date, optional
    deadline: date, optional
    tags: list, optional
    checklist_items: list, optional
    project_id: str, optional
    project_name: str, optional
    heading: str, optional
    completed: bool, optional
    canceled: bool, optional
    """
    task = create_task(title, **kwargs)
    add_items([task])
