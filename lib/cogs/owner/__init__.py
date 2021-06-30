from .owner import Owner

def setup(client):
    client.add_cog(Owner(client))