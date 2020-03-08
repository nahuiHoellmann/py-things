from things import create_task
import json


def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


def test_create_task():

    task = create_task(
            title="Research",
            project_name="Travel",
            checklist_items=[
                "Transport from airport",
                ("Hotels", True)
            ]
        )
    print(json.dumps(task, indent=4))
    expected = {
        "type": "to-do",
        "attributes": {
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
    }

    assert ordered(task) == ordered(expected)