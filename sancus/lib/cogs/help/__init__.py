from .help import helpButtons

def setup(client):
    client.add_cog(helpButtons(client))