from .filter import Filter

def setup(client):
    client.add_cog(Filter(client))