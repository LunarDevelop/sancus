from .meta import Meta

def setup(client):
    client.add_cog(Meta(client))