from .mod import Mod
from .usercmds import userCmds

def setup(client):
    client.add_cog(Mod(client))
    client.add_cog(userCmds(client))