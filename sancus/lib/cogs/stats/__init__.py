from .stats import Stats

def setup(client):
    client.add_cog(Stats(client))