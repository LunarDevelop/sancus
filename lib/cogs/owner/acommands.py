from discord.ext.commands import command, Cog, is_owner, group

import json

def owner_check(ctx):
    if ctx.author.id == 268035643760836608:
        return True

class Anime(Cog):

    @group(name="anime")
    async def _anime_(self, ctx):
        pass

    @_anime_.command()
    @is_owner()
    async def rename(self, ctx, TYPE, ID,*, newname):
        """Change the name of a waifu or husbando

        Args:
            TYPE : waifu or husbando
            ID (int): ID for said waifu or husbando
            newname (string): New name for them
        """

        with open(f"data/images/anime/{TYPE}.json", 'r') as f:
            data = json.load(f)

        for instance in data:
            ids= instance['id']

            if int(ids)==int(ID):

                instance['name'] = newname

        with open(f"data/images/anime/{TYPE}.json",'w') as f:
            json.dump(data, f, indent=4)
        
        await ctx.send(f"{ID} has been renamed to {newname}")

    @_anime_.command()
    @is_owner()
    async def relink(self, ctx, TYPE, ID, newlink):
        """Relink a waifu or husbando image to a new link

        Args:
            TYPE : waifus or husbandos
            ID (int): ID for said waifu or husbando
            newlink (https link): New link for them
        """ 

        with open(f"data/images/anime/{TYPE}.json", 'r') as f:
            data = json.load(f)

        for instance in data:
            ids= instance['id']

            if int(ids)==int(ID):

                instance['link'] = newlink

        with open(f"data/images/anime/{TYPE}.json",'w') as f:
            json.dump(data, f, indent=4)

        await ctx.send(f"{ID}'s link has changed to {newlink}")

    @_anime_.command()
    @is_owner()
    async def remove(self, ctx, TYPE, ID):
        with open(f"data/images/anime/{TYPE}.json") as f:
            data = json.load(f)

        for e in range(len(data)):
            if data[e].get('id') == int(ID):
                data.pop(e)

        with open(f"data/images/anime/{TYPE}.json",'w') as f:
            json.dump(data, f, indent=4)

        await ctx.send(f"{ID} has been removed")

    @_anime_.command()
    @is_owner()
    async def add(self, ctx, TYPE, *, Links):
        """Add images to a anime image

        Args:
        TYPE: waifus or husbandos
        Links (HTML): Links of images being uploaded
        """
        with open(f"data/images/anime/{TYPE}.json", 'r') as f:
            data = json.load(f)

        try:

            LINKS = Links.split("\n")

            for links in LINKS:
                instance = {'id': (len(data)), 'name' : 'rename me', 'link' : links}       
                data.append(instance)
        
        except:
            instance = {'id': (len(data) + 1), 'name' : 'rename me', 'link' : links[0]}       
            data.append(instance)

            await ctx.send("Cannot upload. Make sure name and link are include next to each other with a space separating them, And new links are on a separate line")

        with open(f"data/images/anime/{TYPE}.json", 'w') as f:
            json.dump(data, f, indent=4)

        await ctx.send("Uploaded")