from .logging import Logging

def setup(client):
    client.add_cog(Logging(client))