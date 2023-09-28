"""
This file contains the main program.  It will apply a 'work' label to any task beneath a todoist projects
that is colored (that is:  The color of the parent project) a specific color.  Like that of your company's corporate
color
"""

from todoist_api_python.api import TodoistAPI
import os
import sys
import json

DEFAULT_WORK_PROJECT_COLOR = "sky_blue" # This should match the 'color' property of a Project object returned by the API
DEFAULT_WORK_LABEL_NAME = "Lendio" #TODO:  Set this to the right label name


def main(work_project_color: str, work_label_name: str, todoist_api_token: str):
    """
    This is the main program
    :return:
    """
    # First, read the API token
    if os.path.isfile(todoist_api_token):

        # This is a file.  Read the token out of it.  But only if it's sufficiently locked down
        perms = oct(os.stat(todoist_api_token)[0])[-3:]
        owner_perm = int(perms[0])
        group_perm = int(perms[1])
        world_perm = int(perms[2])

        ok_owner_perms = (4, 6)
        ok_group_perms = (4, 0)
        ok_world_perms = (0,)

        # Roll over and die if the file permissions are too broad
        if owner_perm not in ok_owner_perms or group_perm not in ok_group_perms or world_perm not in ok_world_perms:
            raise ValueError(f"The file permissions on the file are too broad.  They are {perms}")

        with open(todoist_api_token, 'r') as f:
            todoist_api_token = f.read().strip()
        print(f"Read Todoist API token out of file '{todoist_api_token}'")
    else:
        todoist_api_token = todoist_api_token

    # Instantiate the API
    api = TodoistAPI(todoist_api_token)

    # Get projects
    all_projects = api.get_projects()
    applicable_projects = [ p.id for p in all_projects if p.color == work_project_color ]

    # Get tasks
    all_tasks = api.get_tasks()
    applicable_tasks = [ t for t in all_tasks if t.project_id in applicable_projects ]

    # # Ensure the label exists
    # all_labels = api.get_labels()
    # label_exists = False
    # for l in all_labels:
    #     if l.name == work_label_name:
    #         label_exists = True
    #         break
    # if label_exists is False:
    #

    # Apply the label to the tasks
    for t in applicable_tasks:
        task_id = t.id
        existing_labels = t.labels
        if work_label_name in existing_labels:
            print(f"Task '{t.content}' already has the label '{work_label_name}' applied.  Skipping")
            continue
        else:
            new_labels = existing_labels.append(work_label_name)

        api.update_task(task_id=task_id, labels=[work_label_name])
        print(f"Applied label '{work_label_name}' to task '{t.content}' (ID: '{task_id}')")

    print("!")



if __name__ == '__main__':

    # Read config object
    with open('config.json', 'r') as f:
        config = json.load(f)
    api_token = config['config']['todoist_api_token']  # Don't put secrets in VC!  Make this a symlink to somewhere out-of-project!
    work_project_color = config['config']['work_project_color']
    work_label_name = config['config']['work_label_name']

    main(todoist_api_token=api_token, work_project_color=work_project_color, work_label_name=work_label_name)
