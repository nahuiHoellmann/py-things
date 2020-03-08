import subprocess
import urllib.parse
import json
from dataclasses import dataclass, asdict
from datetime import date


def __build_url(data):
    url = "".join([
        'things:///json?data=',
        urllib.parse.quote_plus(json.dumps(data, separators=(',', ':')))
    ])

    return url


def __call_things_api(data):
    url = __build_url(data)
    subprocess.call(["open", url])


def __restructureTask(attributes):
    if attributes['checklist_items']:
        for chl_item in attributes['checklist_items']:
            if isinstance(chl_item, str):
                chl_attr = {
                    "title": chl_item
                }
            else:
                assert isinstance(chl_item, dict)
                chl_attr = chl_item
                if not chl_attr["completed"]:
                    del chl_attr["completed"]
                if not chl_attr["canceled"]:
                    del chl_attr["canceled"]

            attributes.setdefault("checklist-items", []).append({
                "type": "checklist-item",
                "attributes": chl_attr
            })
    attributes["list-id"] = attributes["project_id"]
    attributes["list"] = attributes["project_name"]
    del attributes['checklist_items']
    del attributes["project_id"]
    del attributes["project_name"]
    keys = [key for key in attributes]
    for key in keys:
        if not attributes[key]:
            del attributes[key]


def __parse_tasks(items, project=None):
    data = []
    for task in items:
        if isinstance(task, str):
            attributes = {
                "title": task
            }
        elif isinstance(task, Task):
            attributes = asdict(task)
            __restructureTask(attributes)
        else:
            raise TypeError

        if project and not attributes["list"]:
            attributes["list"] = project

        data.append({
            "type": "to-do",
            "attributes": attributes
        })
    return data


def add(items, project=None):
    data = __parse_tasks(items, project=None)
    __call_things_api(data)


# @dataclass
# class Project():
#     name: str
#     title: str
#     notes: str = None
#     when: date = None
#     deadline: date = None
#     tags: list = None
#     area_id: str = None
#     area: str = None
#     completed: bool = None
#     canceled: bool = None

# @dataclass
# class Heading():
#     title: str

@dataclass
class ChecklistItem():
    title: str
    completed: bool = None
    canceled: bool = None


@dataclass
class Task():
    title: str
    notes: str = None
    when: date = None
    deadline: date = None
    tags: list = None
    checklist_items: list = None
    project_id: str = None
    project_name: str = None
    heading: str = None
    completed: bool = None
    canceled: bool = None


# All Functions from here on are for test purposes


def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


def test_add():

    tasks = [
        "Einfuehrung Differenzverstaerker",
        Task(
            title="DV - Gleichtaktverstaerkung",
            project_id="SOMEID",
            canceled=True,
            completed=False
        ),
        Task(
            title="Research",
            project_name="Travel",
            checklist_items=[
                "Transport from airport",
                ChecklistItem(
                    title="Hotels",
                    completed=True
                )
            ]
        )
    ]

    # assert isinstance(__call_things_api, Mock)
    add(tasks)
    # __call_things_api.assert_called_once()
    # args, _ = __call_things_api.call_args
    # assert len(args) == 1

    # expected = [
    #     {
    #         "type": "to-do",
    #         "attributes": {
    #             "title": "Einfuehrung Differenzverstaerker"
    #         }
    #     },
    #     {
    #         "type": "to-do",
    #         "attributes": {
    #             "title": "DV - Gleichtaktverstaerkung",
    #             "canceled": True,
    #             "list-id": "SOMEID"
    #         }
    #     },
    #     {
    #         "type": "to-do",
    #         "attributes": {
    #             "title": "Research",
    #             "checklist-items": [
    #                 {
    #                     "type": "checklist-item",
    #                     "attributes": {
    #                         "title": "Transport from airport"
    #                     }
    #                 },
    #                 {
    #                     "type": "checklist-item",
    #                     "attributes": {
    #                         "title": "Hotels",
    #                         "completed": True
    #                     }
    #                 }
    #             ],
    #             "list": "Travel"
    #         }
    #     }
    # ]

    # assert ordered(args[0]) == ordered(expected)


def test_restructure():

    task = Task(
            title="Research",
            project_name="Travel",
            checklist_items=[
                "Transport from airport",
                ChecklistItem(
                    title="Hotels",
                    completed=True
                )
            ]
        )
    expected = {
        "title": "Research",
        "list": "Travel",
        "checklist-items": [
            {
                "type": "checklist-item",
                "attributes": {
                    "title": "Hotels",
                    "completed": True
                }
            },
            {
                "type": "checklist-item",
                "attributes": {
                    "title": "Transport from airport"
                }
            }
        ]
    }
    result = asdict(task)
    __restructureTask(result)

    assert ordered(result) == ordered(expected)
test_add()