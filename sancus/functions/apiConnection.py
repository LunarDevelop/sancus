import requests, json

from .consoleColours import *
from .objects import *

GUILDURL = "https://solarbam.online/api/sancus/guild"

class ApiConnection():

    class guild():
        """An entire class for getting the guild objects for Sancus"""

        def get():
            """A simple method to get all guilds currently in the database for Sancus"""

            request = requests.get(GUILDURL)

            if request.status_code == 200:
                print(f"{colours.OKGREEN}Object has been received from the API{colours.ENDC}")
                return request.json()

            if request.status_code == 500:
                print (f"{colours.FAIL}Error Code 500; Internal Server Error{colours.ENDC}")

            print(f"{colours.FAIL}Bad request{colours.ENDC}")

        def getId(guildID):
            """A simple method to get guild with the id, from the database, for Sancus"""

            request = requests.get(url=GUILDURL+ f"/{guildID}")

            if request.status_code == 200:
                print(f"{colours.OKGREEN}Object has been received from the API{colours.ENDC}")
                return request.json()

            if request.status_code == 500:
                print (f"{colours.FAIL}Error Code 500; Internal Server Error{colours.ENDC}")

            print(f"{colours.FAIL}Bad request{colours.ENDC}")

        def post(guildObject : guildObject):

            newDict = guildObject.__dict__

            for key, value in dict(newDict).items():
                if value == None:
                    del newDict[key]
                    
            request = requests.post(url=GUILDURL, json=newDict)

            if request.status_code == 200:
                print(f"{colours.OKGREEN}Object has been posted to the API{colours.ENDC}")
                return

            if request.status_code == 500:
                print (f"{colours.FAIL}Error Code 500; Internal Server Error{colours.ENDC}")

            print(f"{colours.FAIL}Bad request, {request}{colours.ENDC}")
        
        def delete(guildID):

            request = requests.delete(url=GUILDURL+ f"/{guildID}", json= {"guildID" : str(guildID)})

            if request.status_code == 200:
                print(f"{colours.OKGREEN}Object has been delete to the API{colours.ENDC}")
                return request.json()

            if request.status_code == 500:
                print (f"{colours.FAIL}Error Code 500; Internal Server Error{colours.ENDC}")

            print(f"{colours.FAIL}Bad request{colours.ENDC}")
        
        def put(guildObject : guildObject):
            
            GUILD = requests.get(GUILDURL+f"/{guildObject.guildID}").json()
            oldDict = GUILD

            newDict = guildObject.__dict__
            guildID = newDict["guildID"]
 
            for key, value in dict(newDict).items():
                if value == None:
                    newDict[key] = oldDict[key]
                    
                if key == "guildID":
                    newDict[key] = str(value)
                    
            request = requests.put(url=GUILDURL+ f"/{guildID}", json=newDict)

            if request.status_code == 200:
                print(f"{colours.OKGREEN}Object has been put to the API{colours.ENDC}")
                return request.json()

            if request.status_code == 500:
                print (f"{colours.FAIL}Error Code 500; Internal Server Error{colours.ENDC}")
                return

            else:
                print(f"{colours.FAIL}Bad request{colours.ENDC}")

class APIconfig():
    """To keep a object of all configs for the bot so the bot does not have to call the api each time. When a setting has been changed request to update this config class"""

    def __init__(self) -> None:
        """__init__ function to keep all the data in the object"""

        self.guilds = ApiConnection.guild.get()

    def __update__(self) -> None:
        """Update the object so it has the updated information"""

        self.guilds = ApiConnection.guild.get()
        
        return self.guilds