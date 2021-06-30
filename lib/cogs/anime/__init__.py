from .anime import Anime

def setup(client):
    client.add_cog(Anime(client))