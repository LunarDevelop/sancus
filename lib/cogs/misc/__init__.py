from .misc import Misc

def setup(client):
    client.add_cog(Misc(client))