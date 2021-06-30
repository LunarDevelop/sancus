from .errors import Errors

def setup(client):
    client.add_cog(Errors(client))