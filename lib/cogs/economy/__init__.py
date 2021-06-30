from .economy import Econ

def setup(client):
    client.add_cog(Econ(client))