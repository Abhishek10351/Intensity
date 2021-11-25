import nextcord
from nextcord.ext import commands
from sql import execute, fetch
from random import randrange
import time
from mongo import prefixes

class Utility(commands.Cog):
    def __init__(self, Intensity: commands.Bot):
        self.Intensity = Intensity

    @commands.command(aliases=['emojis'])
    @commands.guild_only()
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def emotes(self, ctx):
        """ Shows all the emojis available in the server"""
        emojis = ctx.guild.emojis
        emotes = ''
        emote_size = 0
        animated = ''
        animated_size = 0
        for i in emojis:
            if i.animated:
                animated += str(i)
                animated_size += 1
            else:
                emotes += str(i)
                emote_size += 1
        await ctx.send(embed=nextcord.Embed(title=f'**Total Emojis:{len(emojis)}\nEmotes:{emote_size}\nAnimated:{animated_size}**', description=emotes + animated, color=nextcord.Colour.random()))

    @commands.command(name='roles')
    @commands.guild_only()
    @commands.cooldown(1, 40, commands.BucketType.channel)
    async def roles(self, ctx: commands.Context):
        """Shows all the roles available in the current server """
        all_roles = [i.mention if i.name !=
                     '@everyone' else i.name for i in ctx.guild.roles]
        all_roles.reverse()
        await ctx.send(embed=nextcord.Embed(title=f'**Roles Available in {ctx.guild.name}**', description='\n'.join(all_roles)))

    @commands.command(name='avatar', aliases=['av', 'pfp'])
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def avatar(self, ctx: commands.Context, member: nextcord.Member=None):
        """Embeds the avatar of the member"""
        user = ctx.author.display_avatar
        member = member or ctx.author
        url = member.display_avatar.url
        embed = nextcord.Embed(title='Avatar\n',)
        embed.set_author(name=f'{member}', icon_url=url)
        embed.set_image(url=url)
        embed.set_footer(
            text=f"Invoked by {ctx.author}", icon_url=user.url)
        await ctx.send(embed=embed)

    @commands.command(name='role', aliases=['roleinfo', 'role-info'])
    @commands.cooldown(1, 10, commands.BucketType.channel)
    async def role(self, ctx, *, _role: nextcord.Role=None):
        if _role is not None:
            _time = _role.created_at
            _time = _time.strftime("%I:%m %p, %B %-d %Y")
            embed = nextcord.Embed(title=_role.name, color=_role.color)
            embed.add_field(name="ID", value=f'**{_role.id}**')
            embed.add_field(name="Created", value=_time)
            embed.add_field(name="Mentionable:", value=_role.mentionable)
            embed.add_field(name="Hoisted", value=f"**{_role.hoist}**")
            await ctx.send(embed=embed)
        if _role is None:
            await ctx.send(embed=nextcord.Embed(description='**Cmmon enter a role**'))

    @commands.command(aliases=['serverinfo', 'server-info'])
    async def server(self, ctx):
        """ Get some details of the server """
        embed = nextcord.Embed(
            title=ctx.guild, color=nextcord.Colour.red())
        embed.add_field(name='Server Owner', value=f'**{ctx.guild.owner}**')
        embed.add_field(
            name='Roles', value=f'**{len(ctx.guild.roles)}**')
        embed.add_field(name='Emojis', value=f'**{len(ctx.guild.emojis)}**')
        embed.add_field(name='Text Channels',
                        value=f'**{len(ctx.guild.text_channels)}**')
        embed.add_field(name='Voice Channels',
                        value=f'**{len(ctx.guild.voice_channels)}**')
        embed.set_thumbnail(url=ctx.guild.icon)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def prefix(self, ctx, new_prefix: str=None):
        """Change my prefix in this server"""
        if new_prefix is None:
            await ctx.send(embed=nextcord.Embed(description='**Enter the new prefix idiot.**', color=0Xff0000))
            return
        if len(new_prefix) > 5:
            await ctx.send(embed=nextcord.Embed(description='**Prefix length can\'t be more than 5 **', color=0Xff0000))
            return
        else:
            old_prefix = prefixes.find_one({"_id":ctx.message.guild.id})
            prefixes.update_one({"_id":ctx.message.guild.id}, {"$set": {"prefix":new_prefix.strip()}})
            await ctx.send(embed=nextcord.Embed(description=f'**Prefix changed in {ctx.guild} from `{old_prefix["prefix"]}` to `{new_prefix.strip()}` **', color=nextcord.Colour.random()))
    
    @commands.command(aliases=["userinfo", "member", "memberinfo"])
    @commands.guild_only()
    async def user(self, ctx, member: nextcord.Member=None):
        member = member or ctx.author
        embed = nextcord.Embed(description=member.mention, colour=member.colour)
        #embed.add_field(name="Permissions", values=)
        embed.add_field(name="Account created", value=member.created_at.strftime("%I:%m %p, %B %d %Y"))
        embed.add_field(name="Joined at", value=member.joined_at.strftime("%I:%m %p, %B %d %Y"))
        
        embed.add_field(name="Roles", value="".join(map(lambda i: i.mention if i.id!=ctx.guild.id else "", member.roles)), inline=False)
        embed.set_author(name=member, icon_url=member.display_avatar.url)
        embed.set_footer(text=f"Invoked by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        embed.set_thumbnail(url=member.display_avatar.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def uptime(self, ctx):
        """ Get the time when the bot was last run """
        await ctx.send(f' Uptime - <t:{int(self.Intensity.starttime)}:F>')
    
    @commands.command(hidden=True)
    @commands.is_owner()
    async def stop(self, ctx):
        """Make the bot go offline"""
        await ctx.send(embed=nextcord.Embed(description="**Closing bot in 1 sec**", colour=nextcord.Colour.random()))
        time.sleep(1)
        await self.Intensity.close()


def setup(Intensity):
    Intensity.add_cog(Utility(Intensity))
