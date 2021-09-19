from configparser import ConfigParser
from functions.objects import guildObject, userObject, reactObject

import requests
import json

api_ini = "sancus/data/api.ini"
api_version = "v1"


class connectionDb():

    def __init__(self):
        api_data = ConfigParser()
        with open(api_ini) as f:
            api_data.read_file(f)

        self.uri = api_data["DEFAULT"]["uri"]
        self.headers = {"Authorization": api_data["DEFAULT"]["auth"]}

    # GET methods

        # GET a single guild
    def get_config_guild(self, id):
        uri = self.uri+f"/{api_version}/sancus/guilds/{id}"
        r = requests.get(uri, headers=self.headers)
        if r.status_code == 200:
            return r.json()["Content"]
        else:

            return None

        # GET list of all guilds
    def get_config_guilds(self):
        uri = self.uri+f"/{api_version}/sancus/guilds"
        r = requests.get(uri, headers=self.headers)
        if r.status_code == 200:
            return r.json()["Content"]
        else:

            return None

        # GET a single user
    def get_config_user(self, id):
        uri = self.uri+f"/{api_version}/sancus/users/{id}"
        r = requests.get(uri, headers=self.headers)
        if r.status_code == 200:
            return r.json()["Content"]
        else:

            return None

        # GET list of all Users
    def get_config_users(self):
        uri = self.uri+f"/{api_version}/sancus/users"
        r = requests.get(uri, headers=self.headers)
        if r.status_code == 200:
            return r.json()["Content"]
        else:

            return None

        # GET a single reacts
    def get_config_react(self, id):
        uri = self.uri+f"/{api_version}/sancus/reacts/{id}"
        r = requests.get(uri, headers=self.headers)
        if r.status_code == 200:
            return r.json()["Content"]
        else:

            return None

        # GET list of all reacts
    def get_config_reacts(self):
        uri = self.uri+f"/{api_version}/sancus/reacts"
        r = requests.get(uri, headers=self.headers)
        if r.status_code == 200:
            return r.json()["Content"]
        else:

            return None

        # GET config
    def get_config_config(self):
        uri = self.uri+f"/{api_version}/sancus/config"
        r = requests.get(uri, headers=self.headers)
        if r.status_code == 200:
            return r.json()["Content"]
        else:

            return None

    # POST Methods

        # POST guild
    def post_config_guild(self, guild: guildObject):
        uri = self.uri+f"/{api_version}/sancus/guilds"
        r = requests.post(uri, headers=self.headers,
                          json=json.dumps(guild.__dict__))
        if r.status_code == 200:
            return r.json()["Content"]
        else:

            return None

    def post_config_user(self, user: userObject):
        uri = self.uri+f"/{api_version}/sancus/users"
        r = requests.post(uri, headers=self.headers,
                          json=json.dumps(user.__dict__))
        if r.status_code == 200:
            return r.json()["Content"]
        else:

            return None

    def post_config_react(self, react: reactObject):
        uri = self.uri+f"/{api_version}/sancus/reacts"
        r = requests.post(uri, headers=self.headers,
                          json=json.dumps(react.__dict__))
        if r.status_code == 200:
            return r.json()["Content"]
        else:

            return None

    # PUT Methods

        # PUT guild
    def put_config_guild(self, id, input):
        uri = self.uri+f"/{api_version}/sancus/guilds"
        data = {"id": id, "input": input}

        r = requests.put(uri, headers=self.headers,
                         json=json.dumps(data))
        if r.status_code == 200:
            return r.json()
        else:

            return None

    def put_config_user(self, id, input):
        uri = self.uri+f"/{api_version}/sancus/users"
        data = {"id": id, "input": input}
        r = requests.put(uri, headers=self.headers,
                         json=json.dumps(data))
        if r.status_code == 200:
            return r.json()
        else:

            return None

    def put_config_react(self, id, name, input):
        uri = self.uri+f"/{api_version}/sancus/reacts"
        data = {"id": id, "name": name, "input": input}

        r = requests.put(uri, headers=self.headers,
                         json=json.dumps(data))
        if r.status_code == 200:
            return r.json()
        else:

            return None

        # PUT config

    def put_config_config(self, input):
        uri = self.uri+f"/{api_version}/sancus/guilds"
        data = {"id": 0, "input": input}

        r = requests.put(uri, headers=self.headers,
                         json=json.dumps(data))
        if r.status_code == 200:
            return r.json()
        else:

            return None

    # DELETE Methods

        # DELETE guild
    def delete_config_guild(self, id):
        uri = self.uri+f"/{api_version}/sancus/guilds"
        data = {"id": id}

        r = requests.delete(uri, headers=self.headers,
                            json=json.dumps(data))
        if r.status_code == 200:
            return r.json()
        else:

            return None

    def delete_config_user(self, id):
        uri = self.uri+f"/{api_version}/sancus/users"
        data = {"id": id}

        r = requests.delete(uri, headers=self.headers,
                            json=json.dumps(data))
        if r.status_code == 200:
            return r.json()
        else:

            return None

    def delete_config_react(self, id, name):
        uri = self.uri+f"/{api_version}/sancus/reacts"
        data = {"id": id, "name": name}

        r = requests.delete(uri, headers=self.headers,
                            json=json.dumps(data))
        if r.status_code == 200:
            return r.json()
        else:

            return None
