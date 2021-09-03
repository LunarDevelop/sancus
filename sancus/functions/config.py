import json
import discord

from configparser import ConfigParser, NoOptionError, NoSectionError


class config():
    """

    OLD system please use the new API if can :)

    """

    def __init__(self) -> None:
        self.config_ = ConfigParser()
        self.USERFile = ConfigParser()

        with open("./data/config.ini", 'r') as f:
            self.config_.read_file(f)

        with open("./data/users.ini", 'r') as userfile:
            self.USERFile.read_file(userfile)

        "SETTING THE DEFAULT SETTINGS"

        self.DEFAULTS = {
            "prefix": "s!",
            "log_channel": 0,
            "action_channel": 0,
            "filter": 0,
            "filter_type": 0,
            "welcome_style": 0,
            "welcome_channel": 0,
            "welcome_background": "#ffffff",
            "welcome_icon": 0,
            "welcome_banner": 0,
            "welcome_text_color": "#000000",
            "welcome_username_color": "#000000",
            "welcome_members_color": "#000000"
        }

        self.EMBEDS = {
            "DEFAULT": {
                "main_timeout": "274845",
                "main_cancel": "947BAD",
                "setting_menus": "274845",
                "log_deleted": "FF0000",
                "log_edited": "FFA500",
                "mod_avatar": "947BAD",
                "mod_kick": "947BAD",
                "mod_ban": "947BAD",
                "mod_unban": "947BAD",
                "member_join": "6666FF",
                "member_leave": "6666FF",
                "member_update": "83f3e6",
                "anime_waifus": "d45004",
                "anime_husbandos": "d45004",
                "anime_my_waifu": "d45004",
                "anime_my_husbando": "d45004",
                "anime_image_anime": "e3b7d2",
                "anime_image_wallpaper": "e3b7d2",
                "anime_image_azurlane": "e3b7d2",
                "anime_image_nekopara": "e3b7d2",
                "anime_totalimages": "e3b7d2",
                "econ_balance": "B2003F",
                "mc_server_online": "81d82e",
                "mc_server_offline": "d8302e",
            },

        }

        self.TIMEOUTS = {
            "DEFAULT": {
                "payday": 3600,
                "beg": 120,
                "gamble": 120,
                "waifus": 0,
                "husbandos": 0
            },

        }

        self.USERS = {

        }

        self.REACTIONS = {

        }

        self.get_all()
        self.save()

    def get_all(self):
        with open("./data/config.ini", 'r') as f:
            self.config_.read_file(f)

        for section in self.config_.sections():
            if "_embeds" in section and section != "USERS" and "_timeouts" not in section:
                self.EMBEDS[section[:-7]] = {}
                for option in self.config_.options(section):
                    if self.EMBEDS['DEFAULT'].get(option) != None:
                        self.EMBEDS[section[:-7]
                                    ][option] = self.config_.get(section, option)

            elif "_embeds" not in section and section != "USERS" and "_timeouts" in section:
                self.TIMEOUTS[section[:-9]] = {}
                for option in self.config_.options(section):
                    if self.TIMEOUTS['DEFAULT'].get(option) != None:
                        self.TIMEOUTS[section[:-9]
                                      ][option] = self.config_.get(section, option)

        with open("./data/users.ini", 'r') as usersINI:
            self.USERFile.read_file(usersINI)

            for user in self.USERFile.sections():
                self.USERS[user] = {}
                for option in self.USERFile.options(user):
                    self.USERS[user][option] = self.USERFile.get(user, option)

        with open("./data/reactions.json", "r") as reactionFile:
            self.REACTIONS = json.load(reactionFile)

    def save(self):
        """Saving the entire configuation to the .ini file for save keeping.
        Should be called everytime a change as happened for safety reasons."""

        for section in self.EMBEDS:
            if section != "DEFAULT":
                for option in self.EMBEDS[section]:
                    try:
                        self.config_.set(f"{section}_embeds", str(
                            option), str(self.EMBEDS[section][option]))

                    except NoSectionError:
                        self.config_.add_section(f"{section}_embeds")
                        self.config_.set(f"{section}_embeds", str(
                            option), str(self.EMBEDS[section][option]))

        for section in self.TIMEOUTS:
            if section != "DEFAULT":
                for option in self.TIMEOUTS[section]:
                    try:
                        self.config_.set(f"{section}_timeouts", str(
                            option), str(self.TIMEOUTS[section][option]))

                    except NoSectionError:
                        self.config_.add_section(f"{section}_timeouts")
                        self.config_.set(f"{section}_timeouts", str(
                            option), str(self.TIMEOUTS[section][option]))

        for section in self.USERS:
            str(section)
            for key in self.USERS[section]:
                try:
                    self.USERFile.set(str(section), key, str(
                        self.USERS[section].get(key)))
                except:
                    self.USERFile.add_section(str(section))
                    self.USERFile.set(section, key, str(
                        self.USERS[section].get(key)))

        with open("./data/config.ini", 'w') as f:
            self.config_.write(f)

        with open("./data/users.ini", 'w') as userFile:
            self.USERFile.write(userFile)

        with open("./data/reactionFile", 'w') as reactionFile:
            json.dump(self.REACTIONS, reactionFile, indent=4)

    def embed(self, section, option):
        self.get_all()
        try:
            return int(self.EMBEDS[str(section)][option], 16)

        except:
            return int(self.EMBEDS["DEFAULT"][option], 16)

    def set_embed(self, section, option, value):
        self.EMBEDS[section][option] = value
        self.save()

    def timeout(self, section, option):
        self.get_all()
        try:
            return self.TIMEOUTS[str(section)][option]

        except KeyError:
            return self.TIMEOUTS["DEFAULT"][option]

    def set_timeout(self, section, option, value):
        self.get_all()
        self.TIMEOUTS[section][option] = value
        self.save()

    def user(self, section):
        self.get_all()
        try:
            return self.USERS[str(section)]

        except:
            self.USERS[str(section)] = {'bank': 0, 'wallet': 0}
            self.save()
            return self.USERS[str(section)]

    def set_user(self, section, option, value):
        self.get_all()
        try:
            self.USERS[str(section)][option] = value
        except:
            self.USERS[str(section)] = {}
            self.USERS[str(section)][option] = value
        self.save()

    def add_reaction(self, guildid, messageid, data):
        try:
            self.REACTIONS[guildid][messageid] = data
        except:
            self.REACTIONS[guildid] = []
            self.REACTIONS[guildid][messageid] = data

    def remove_reaction(self, guildid, messageid):
        self.REACTIONS[guildid].pop(messageid)

    """
    General functions for the commands segment
    """

    def add_commands(bot):
        """
        Adding commands to the data
        """

        with open("./data/commands.json") as f:
            data = json.load(f)

        commandsList = []

        for commands in data['commands']:
            commandsList.append(commands['name'])

        for commands in bot.commands:
            if commands.name not in commandsList:
                appendData = {
                    "name": commands.name,
                    "guilds": []
                }

                data['commands'].append(appendData)

                saving_config._savingCommands(data)

    def checking_commands(command, guildID: discord.Guild.id, member: discord.Member):
        """
        Checking to see if user has access to command 
        """

        commands = ""
        guilds = ""

        with open("./data/commands.json") as f:
            data = json.load(f)

        for commands in data['commands']:
            if commands['name'] == command:
                break

        for guilds in commands['guilds']:
            if guilds['ID'] == guildID:

                if member.id in guilds['allowedUsers']:
                    return True

                if member.id not in guilds['disabledUsers']:
                    return False

                for roles in member.roles:
                    if roles.id in guilds['allowedRoles']:
                        return True

                    if roles.id in guilds['disabledRoles']:
                        return False

        return True

    def disable_command_roles(command, guildID: discord.Guild.id, role):
        with open("./data/commands.json") as f:
            data = json.load(f)

        for commands in data['commands']:
            if commands['name'] == command:
                break

        for guilds in commands['guilds']:
            if guilds['ID'] == guildID:
                if role.id in guilds['disabledRoles']:
                    return
                else:
                    guilds['disabledRoles'].append(role.id)
                    return

        appenddata = {
            "ID": guildID,
            "allowedUsers": [],
            "disabledUsers": [],
            "allowedRoles": [],
            "disabledRoles": [role.id]
        }

        commands['guilds'].append(appenddata)

        saving_config._savingCommands(data)

    def enable_command_roles(command, guildID: discord.Guild.id, role):
        with open("./data/commands.json") as f:
            data = json.load(f)

        for commands in data['commands']:
            if commands['name'] == command:
                break

        for guilds in commands['guilds']:
            if guilds['ID'] == guildID:
                if role.id in guilds['enableRoles']:
                    return
                else:
                    guilds['enableRoles'].append(role.id)
                    return

        appenddata = {
            "ID": guildID,
            "allowedUsers": [],
            "disabledUsers": [],
            "allowedRoles": [role.id],
            "disabledRoles": []
        }

        commands['guilds'].append(appenddata)

        saving_config._savingCommands(data)

    def disable_command_Users(command, guildID: discord.Guild.id, userID):
        with open("./data/commands.json") as f:
            data = json.load(f)

        for commands in data['commands']:
            if commands['name'] == command:
                break

        for guilds in commands['guilds']:
            if guilds['ID'] == guildID:
                if userID in guilds['disabledUsers']:
                    return
                else:
                    guilds['disabledUsers'].append(userID)
                    return

        appenddata = {
            "ID": guildID,
            "allowedUsers": [],
            "disabledUsers": [userID],
            "allowedRoles": [],
            "disabledRoles": []
        }

        commands['guilds'].append(appenddata)

        saving_config._savingCommands(data)

    def enable_command_Users(command, guildID: discord.Guild.id, userID):
        with open("./data/commands.json") as f:
            data = json.load(f)

        for commands in data['commands']:
            if commands['name'] == command:
                break

        for guilds in commands['guilds']:
            if guilds['ID'] == guildID:
                if userID in guilds['enableUsers']:
                    return
                else:
                    guilds['enableUsers'].append(userID)
                    return

        appenddata = {
            "ID": guildID,
            "allowedUsers": [userID],
            "disabledUsers": [],
            "allowedRoles": [],
            "disabledRoles": []
        }

        commands['guilds'].append(appenddata)

        saving_config._savingCommands(data)
