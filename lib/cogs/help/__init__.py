from .help import Help, helpButtons

def setup(client):
    #client.add_cog(Help(client))
    client.add_cog(helpButtons(client))