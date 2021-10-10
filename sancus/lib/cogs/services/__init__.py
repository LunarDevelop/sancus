from .services import services

def setup(client):
    client.add_cog(services(client))