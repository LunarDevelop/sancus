from .games import Games

def setup(client):
    client.add_cog(Games(client))