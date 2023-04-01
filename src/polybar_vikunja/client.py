import argparse
import json
import os
import requests

from .config_helper import PolybarVikunjaConfig
from .popups import ConfigPopup, RemainingTodosPopup


class PolybarVikunjaClient():

    def __init__(self, *args, **kwargs):
        '''
        :kwarg config_file: String path relative to ~/ of a config file to load.
        '''
        self.config_file = kwargs.get(
            'config_file',
            '.polybar_vikunja_config.json'
        )
        self.config = PolybarVikunjaConfig(config_file=self.config_file)

        self.base_url = self.config.get(
            'base_url',
            kwargs.get('base_url', None)
        )
        self.username = self.config.get(
            'username',
            kwargs.get('username', None)
        )
        self.password = self.config.get(
            'password',
            kwargs.get('password', None)
        )
        self.default_list = self.config.get(
            "default_list",
            1
        )

        self.login()

    def login(self, refresh_token=False):
        '''
        Logs in to the Vikunja instance using your config.
        '''
        self.jwt = self.config.get('jwt', None)

        if not self.jwt or refresh_token:
            login_url = self.base_url + '/api/v1/login'
            response = requests.post(
                login_url,
                headers={
                    "Content-Type": "application/json"
                },
                json={
                    "username": self.username,
                    "password": self.password
                }
            )

            self.jwt = response.json()["token"]
            self.config.set("jwt", self.jwt)

    def list_todo_lists(self):
        '''
        Returns a dict of list names to IDs.
        '''
        response = requests.get(
            self.base_url + "/api/v1/projects",
            headers={
                "Authorization": f"Bearer {self.jwt}"
            }
        )

        response = response.json()
        if "message" in response and response["message"] == "invalid or expired jwt":
            self.login(refresh_token=True)
            return self.list_todo_lists()
        else:
            return response

    def list_list_contents(self):
        response = requests.get(
            self.base_url + f"/api/v1/projects/{self.default_list}/tasks",
            headers={
                "Authorization": f"Bearer {self.jwt}"
            }
        )

        response = response.json()
        if "message" in response and response["message"] == "invalid or expired jwt":
            self.login(refresh_token=True)
            return self.list_list_contents()
        else:
            return response

    def get_remaining_todos(self):
        response = requests.get(
            self.base_url + f"/api/v1/projects/{self.default_list}/tasks",
            headers={
                "Authorization": f"Bearer {self.jwt}"
            },
            params={
                "filter_by": "done",
                "filter_value": "false",
                "filter_comparator": "equals"
            }
        )

        response = response.json()
        if "message" in response and response["message"] == "invalid or expired jwt":
            self.login(refresh_token=True)
            return self.get_remaining_todos()
        else:
            return response


    def get_todo_count(self):
        return len(self.get_remaining_todos())

    def mark_todo_complete_status(self, todo_id, is_complete):
        response = requests.post(
            self.base_url + f"/api/v1/tasks/{todo_id}",
            headers={
                "Authorization": f"Bearer {self.jwt}"
            },
            json={
                "done": True,
            }
        )

        response = response.json()
        if "message" in response and response["message"] == "invalid or expired jwt":
            self.login(refresh_token=True)
            return self.mark_todo_complete_status(todo_id, is_complete)
        else:
            return response


def first_run():
    '''
    Runs the first time polybar-vikunja is initialized. Gives a basic
    interactive menu and asks the user for details to init the config file.
    '''
    print("\tWelcome to polybar-vikunja!")
    print("This script will set up the initial config file for you.")
    print("WARNING: This script *will* store your credentials in plaintext!")

    config = {}

    response = input("Vikunja Base URL: (e.g. https://try.vikunja.io) ")
    config['base_url'] = response

    response = input("Username: ")
    config['username'] = response

    response = input("Password: ")
    config['password'] = response

    client = PolybarVikunjaClient(
        base_url=config['base_url'],
        username=config['username'],
        password=config['password']
    )

    try:
        client.login()
    except Exception as e:
        print("Problem with your config, try again!")
        print(e)
        first_run()

        return

    # Now set the default list:
    lists = {
        e["title"]: e["id"] for e in client.list_todo_lists()
    }

    print("Lists:")
    for title in lists:
        print(f"\t{title} ({lists[title]})")

    list_id = input("What list number would you like to watch? ")
    config["default_list"] = str(list_id)

    try:
        config_file_dir = client.config_file
        path = os.path.expanduser("~") + f"/{config_file_dir}"
        with open(path, 'w') as fh:
            json.dump(config, fh)
    except Exception as e:
        print(f"Problem writing config file:")
        print(e)

        print("Here's your config to manually add:")
        print(config)

        return


def main():
    parser = argparse.ArgumentParser(
        description='Entrypoint for Vikunja/Polybar integration.'
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--init", action="store_true")
    group.add_argument("--list-todo-lists", action="store_true")
    group.add_argument("--get-todo-count", action="store_true")
    group.add_argument("--list-todos", action="store_true")
    group.add_argument("--config-popup", action="store_true")
    group.add_argument("--show-todos-popup", action="store_true")

    args = parser.parse_args()

    if args.init:
        first_run()

    vikunja_client = PolybarVikunjaClient()

    if args.list_todo_lists:
        print(vikunja_client.list_todo_lists())
    elif args.get_todo_count:
        print(vikunja_client.get_todo_count())
    elif args.list_todos:
        print(vikunja_client.get_remaining_todos())
    elif args.config_popup:
        ConfigPopup(
            lists=vikunja_client.list_todo_lists()
        )
    elif args.show_todos_popup:
        RemainingTodosPopup(vikunja_client)

if __name__ == '__main__':
    main()
