import disnake
from disnake.ext import commands
from random import choice
from disnake.utils import get
from random import choice
from sql import execute, fetch
from typing import Union, Optional
from emojis import no, shocked
from converters import TimeConverter, SlowmodeTimeConverter, TimeoutConverter
import asyncio
import time
from datetime import timedelta, datetime
from errors import SlowmodeError
import re


class Moderation(commands.Cog):
    """ Module for controlling the server and members """

    def __init__(self, Intensity: commands.Bot):
        self.Intensity = Intensity

    @commands.command(name='warn')
    @commands.guild_only()
    @commands.cooldown(1, 3)
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, member: disnake.Member = None, *, reason):
        if member is None:
            await ctx.send(embed=disnake.Embed(description="**Idiot who do u wanna warn**", color=0Xff0000))
        elif member.bot:
            await ctx.reply(embed=disnake.Embed(description='**Stupid don\'t u know I can\'t dm a bot**', color=0Xff0000))
        else:
            message = disnake.Embed(
                description=f'**You have been warned in {ctx.guild} \nReason: {reason}\nModerator: {ctx.author.mention}**', color=0Xff0000)
            reply = disnake.Embed(
                description=f'**{member.mention} has been warned.\nReason: {reason}**', color=0Xff0000)
            await member.send(embed=message)
            await ctx.send(embed=reply)

    @warn.error
    async def warn_error(self, ctx, error):
        a = getattr(error, "original",  error)
        if isinstance(a, disnake.Forbidden):
            await ctx.send(embed=disnake.Embed(description='**That idiot has blocked me so I couldn\'t dm**'))
        else:
            await ctx.send(error)

    @commands.group(name='slowmode', aliases=['sm', 'slow'])
    @commands.cooldown(1, 10, commands.BucketType.channel)
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    @commands.guild_only()
    async def slowmode(self, ctx):
        """Change the slowmode delay in the current channel"""
        pass

    @slowmode.command(name="set", aliases=["change"])
    async def set_sm(self, ctx: commands.Context, _time: commands.Greedy[SlowmodeTimeConverter] = None):
        """Sets a slowmode in the current channel"""
        def get_slowmode_time(__seconds) -> str:
            message = ""
            if (__seconds >= 3600) and (__seconds % 21600 != 0):
                hours = __seconds // 3600
                message += f' {int(hours)} hours'
            if (__seconds >= 60) and (__seconds % 3600 != 0):
                minutes = (__seconds // 60) % 60
                message += f' {int(minutes)} minutes'
            if (__seconds % 60 != 0) or (__seconds < 60):
                seconds = __seconds % 60
                message += f' {int(seconds)} seconds'
            return message
        
        delta = timedelta()
        for i in _time:
            try:
                delta += i
            except:
                await ctx.send("**Invalid parameters provided**")
                return
        __seconds = delta.seconds
        message = f"**Set the slowmode in {ctx.channel.mention} to {get_slowmode_time(__seconds)}**"
        if __seconds == 0:
            if ctx.channel.slowmode_delay:
                await ctx.channel.edit(slowmode_delay=0)
                await ctx.send(f"**Slowmode turned off in {ctx.channel.mention}**")
            else:
                await ctx.send(f'**Currently there is no slowmode in {ctx.channel.mention}**')
            return
        elif 0 <= __seconds <= 21600:
            await ctx.channel.edit(slowmode_delay=int(delta.seconds))
            await ctx.send(message)
        else:
            await ctx.send('**You can only input time from 0 seconds to 6 hours**')

    @slowmode.command(aliases=["turnoff", "off"])
    async def reset(self, ctx):
        """Reset the slowmode in the current channel"""
        def get_slowmode_time(seconds) -> str:
            message = ""
            if (seconds >= 3600) and (seconds % 21600 != 0):
                hours = __seconds // 3600
                message += f' {int(hours)} hours'
            if (seconds >= 60) and (seconds % 3600 != 0):
                minutes = (seconds // 60) % 60
                message += f' {int(minutes)} minutes'
            if (seconds % 60 != 0) or (seconds < 60):
                seconds = seconds % 60
                message += f' {int(seconds)} seconds'
            return message
        if ctx.channel.slowmode_delay:
            await ctx.send(f"**The slowmode in {ctx.channel.mention} is {get_slowmode_time(ctx.channel.slowmode_delay)}**")
            return
        else:
            await ctx.send(f'**Currently there is no slowmode in {ctx.channel.mention}**')
            return

    @commands.command(name='muterole')
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(manage_roles=True)
    @commands.guild_only()
    async def muterole(self, ctx, role: disnake.Role):
        me = ctx.guild.me
        if role.is_default() or role.is_integration() or role.is_bot_managed() or role.is_premium_subscriber() or role is None:
            await ctx.send(embed=disnake.Embed(description=f'**Please enter a valid role to save as Mute role**', color=0Xff0000))
            return
        elif me.top_role <= role:
            await ctx.send(embed=disnake.Embed(description=f'**{choice(no)} I can\'t set that role as muted role because it has a higher position than my top role**', color=0Xff0000))
            return
        elif (not ctx.author == ctx.guild.owner) and ctx.author.top_role <= role:
            await ctx.send(embed=disnake.Embed(description=f'**You can\'t set roles higher than you as muted role**', color=0Xff0000))
            return
        role_id = fetch(
            f'select role_id from muted_roles where guild_id = {ctx.guild.id}')
        if role_id is None:
            execute(
                f'insert into muted_roles values({ctx.guild.id}, {role.id});')
            await ctx.send(embed=disnake.Embed(description=f'**{role.mention} is saved as a muted role.**', color=0Xff0000))
            return
        elif role_id[0] != role.id:
            muted_role = disnake.utils.get(
                ctx.guild.roles, id=int(role_id[0]))
            execute(
                f'update muted_roles set role_id = {role.id} where guild_id = {ctx.guild.id}')
            await ctx.send(embed=disnake.Embed(description=f'**Mute role changed from {muted_role.mention} to {role.mention}**', color=0Xff0000))
            return
        else:
            await ctx.send(embed=disnake.Embed(description=f'**{role.mention} is already saved as a muted role in this server**', color=0Xff0000))

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True, manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def mute(self, ctx, member: disnake.Member = None, _time: commands.Greedy[TimeConverter] = None, reason="Not Given"):
        """Give users a infraction """
        role_id = fetch(
            f'select role_id from muted_roles where guild_id = ( ? )', ctx.guild.id)
        if role_id is None:
            prefix = fetch(
                f'select role_id from muted_roles where guild_id = {ctx.guild.id} ;')
            await ctx.send(embed=disnake.Embed(description=f'**{ctx.author.mention} I have no muted role configured in {ctx.guild.name}\nUse `[p]muterole role` to do that**'))
            return
        muted_role = disnake.utils.get(ctx.guild.roles, id=int(role_id[0]))
        my_top_role = ctx.guild.me.top_role
        if member is None:
            await ctx.send(embed=disnake.Embed(description='**Idiot enter a member to mute**', color=0Xff0000))
            return
        elif member == ctx.author:
            await ctx.send(embed=disnake.Embed(description='**Dude you can\'t mute yourself**', color=0Xff0000))
            return
        elif member == ctx.guild.me:
            await ctx.send(embed=disnake.Embed(description='**Nah I will not mute myself**', color=0Xff0000))
            return
        elif muted_role in member.roles:
            await ctx.send(embed=disnake.Embed(description=f'**{member.mention} has already been muted**', color=0Xff0000))
            return
        elif member == ctx.guild.owner:
            await ctx.send(embed=disnake.Embed(description=f'**<a:toothless:859342271631458325> I can\'t mute the server owner**', color=0Xff0000))
            return
        elif my_top_role < muted_role:
            await ctx.send(embed=disnake.Embed(description=f"**Damn I can't mute due to muted role position**", color=0Xff0000))
            return
        else:
            if not ctx.author == ctx.guild.owner:
                if ctx.author.top_role >= member.top_role:
                    await ctx.send(embed=disnake.Embed(description=f"**You can't mute members with same top role or higher roles than you**", color=0Xff0000))
                    return
                elif ctx.author.top_role < muted_role:
                    await ctx.send(embed=disnake.Embed(description=f'**You can\'t mute members because of position of the role**', color=0Xff0000))
                    return
            if muted_role in member.roles:
                await ctx.send(embed=disnake.Embed(description=f'{member.mention} is already muted', color=0Xff0000))
                return
            else:
                await member.add_roles(muted_role)
                await ctx.send(embed=disnake.Embed(description=f'{member.mention} has been muted', color=0Xff0000))
                if not member.bot:
                    await member.send(embed=disnake.Embed(description=f'You have been muted in {ctx.guild.name}\nReason:{message}'))

    @commands.command(name='unmute')
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: disnake.Member = None):
        if member is None:
            await ctx.send(embed=disnake.Embed(description=f'**Enter a member to mute idiot.**'))
            return
        role_id = fetch(
            f'select role_id from muted_roles where guild_id = {ctx.guild.id}')
        if role_id is None:
            prefix = fetch(
                f'select role_id from muted_roles where guild_id = {ctx.guild.id} ;')
            await ctx.send(embed=disnake.Embed(description=f'{ctx.author.mention} I have no muted role configured in {ctx.guild.name}\nUse `[p]muterole role` to do that'))
            return
        muted_role = disnake.utils.get(ctx.guild.roles, id=int(role_id[0]))
        my_top_role = ctx.guild.me.top_role
        if member in [ctx.guild.me, ctx.author, ctx.guild.owner]:
            await ctx.send(embed=disnake.Embed(description="**Dude don't be stupid**", color=0Xff0000))
            return
        elif not muted_role in member.roles:
            await ctx.send(embed=disnake.Embed(description=f'**{member.mention} is not muted atm**', color=0Xff0000))
            return
        elif my_top_role < muted_role:
            await ctx.send(embed=disnake.Embed(description=f'**Damn I can\'t unmute due to muted role hiearchy**', color=0Xff0000))
            return
        else:
            if ctx.author == ctx.guild.owner:
                if ctx.author.top_role <= member.top_role:
                    await ctx.send(embed=disnake.Embed(description=f'**You can\'t mute members with same top role as you or with higher roles than you**', color=0Xff0000))
                    return
                elif ctx.author.top_role < muted_role:
                    await ctx.send(embed=disnake.Embed(description=f'**You can\'t unmute members because of muted role position**', color=0Xff0000))
                    return
            if muted_role not in member.roles:
                await ctx.send(embed=disnake.Embed(description=f'**{member.name} is not muted**', color=0Xff0000))
                return
            else:
                await member.remove_roles(muted_role)
                await ctx.send(embed=disnake.Embed(description=f'**{member.mention} has been unmuted**'))

    @commands.command(name='kick')
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: disnake.Member = None, *, reason: Optional[str] = "Not given"):
        """ Kick all those who u don't wanna keep"""
        if member is None:
            await ctx.send(embed=disnake.Embed(description=f'**Enter a member to kick idiot**', color=0Xff0000))
            return
        elif member in [ctx.author, ctx.guild.me, ctx.guild.owner]:
            await ctx.send(embed=disnake.Embed(description=f'**I will never do this <:drake_no:838129333264580608> **', color=0Xff0000))
            return
        else:
            if (not ctx.author == ctx.guild.owner) and (ctx.author.top_role <= member.top_role):
                await ctx.send(embed=disnake.Embed(description=f'**You can\'t kick members with same or higher roles than you**', color=0Xff0000))
                return
            try:
                await member.send(embed=disnake.Embed(description=f'**You have ben kicked from {ctx.guild.name}\nReason: {reason}**', color=0Xff0000))
            except Exception as e:
                pass
            await member.kick(reason=reason)
            await ctx.send(embed=disnake.Embed(description=f'**{member} has been kicked**', color=0Xff0000))

    @commands.command(name='ban')
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.guild_only()
    async def ban(self, ctx, member: disnake.Member, _time: commands.Greedy[TimeConverter] = None, *, reason=None):
        """ Ban members who are not following the rules """
        if member is None:
            await ctx.send(embed=disnake.Embed(description=f'**Pls enter a member to ban**', color=0Xff0000))
            return
        elif member == ctx.author:
            return
        elif member == ctx.guild.me:
            await ctx.send(embed=disnake.Embed(description=f'**Lmao why whould I ban myself**', color=0Xff0000))
            return
        elif ctx.guild.me.top_role <= member.top_role:
            await ctx.send(embed=disnake.Embed(description=f'**{choice(no)} I can\'t ban {member.mention} because of role hiearchy', color=0Xff0000))
            return
        elif member == ctx.guild.owner:
            await ctx.send(embed=disnake.Embed(description=f'** {choice(no)} Damn you can\'t ban the server owner**', color=0Xff0000))
            return
        elif (not ctx.author == ctx.guild.owner) and (ctx.author.top_role <= member.top_role):
            await ctx.send(embed=disnake.Embed(description=f'**You can\'t ban members with roles higher than you**', color=0Xff0000))
            return
        timed = False
        if isinstance(_time, list) and (None in _time):
            await ctx.reply('**Invalid values provided for time**')
            return
        if isinstance(_time, list):
            timed = True
        if not member.bot:
            try:
                await member.send(embed=disnake.Embed(description=f'**You have been banned from {ctx.guild.name}\nReason:{reason}**', color=0Xff0000))
            except:
                pass
        message = f'**{member} has been banned from {ctx.guild.name}**'
        if time:
            message += f'** until <t:{int(time.time() + sum(_time))}:R> **'
            ctx.send(time.time() + sum(_time))
        await member.ban(reason=reason)
        await ctx.send(embed=disnake.Embed(description=message, color=0Xff0000))
        a = timedelta()
        for i in _time:
            a += i 
        await asyncio.sleep(a.seconds)
        await member.unban(reason="Time over")

    @commands.command(name='unban')
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True, send_messages=True)
    @commands.guild_only()
    async def unban(self, ctx, users: commands.Greedy[disnake.User] = None):
        """Unban users if you think they have improved"""
        banned_users = await ctx.guild.bans()
        banned_users = [i.user for i in banned_users]
        users = [i for i in users if i in banned_users]
        for i in users:
            await ctx.guild.unban(i)
        await ctx.send(embed=disnake.Embed(description=f'**Members unbanned**', color=0Xff0000))

    @commands.command(name='nickname', aliases=['nick', 'newnick'])
    @commands.has_permissions(manage_nicknames=True, change_nickname=True)
    @commands.bot_has_permissions(manage_nicknames=True, change_nickname=True)
    @commands.guild_only()
    async def nickname(self, ctx, member: Optional[disnake.Member] = None, *, _nick=None):
        """Change your nickname or a particular member's"""
        if member:
            if (member.top_role >= ctx.author.top_role) and ( (ctx.me.top_role >= ctx.author.top_role) or
            ctx.author.is_owner()) :
                pass
            else:
                return
        member = member or ctx.author
        if len(_nick) > 32:
            await ctx.reply('**Nickname length must be between 0 and 32 characters**')
            return
        try:
            await member.edit(nick=_nick)
        except:
            await ctx.send(f"**I don't have enough perms to change {member}'s nickname**")
            return
        await ctx.reply(f'**Nickname changed to {_nick or member.display_name}**')

    @commands.command(name='purge', aliases=['clean', 'delete'])
    @commands.cooldown(1, 5)
    @commands.has_permissions(manage_messages=True, read_message_history=True)
    @commands.bot_has_permissions(manage_messages=True, read_message_history=True, send_messages=True)
    @commands.guild_only()
    async def purge(self, ctx: commands.Context, command: Union[disnake.Member, disnake.Role, int, str] = None, *, others: Union[int, str] = None):
        """ Clean unwanted messages from the current channel"""
        def check(message):
            """ Checks if a message needs to be purged """
            if isinstance(command, disnake.member.Member):
                return command == message.author
            elif isinstance(command, disnake.role.Role):
                return command in message.author.roles
            elif isinstance(command, str):
                if command.lower() in ['bot', 'bots']:
                    return message.author.bot
                elif commands.lower() == 'all':
                    return True
                elif command.lower() in ['user', 'users']:
                    return not message.author.bot
                elif command.lower() in ['contains', 'contain']:
                    return str(others).lower() in message.content
                elif command.lower() in ['startswith', 'startwith']:
                    return message.content.startswith(str(others))
                elif command.lower() in ['endswith', 'endwith']:
                    return message.content.endswith(str(others))
                else:
                    return False
            elif isinstance(command, int):
                return True

        def limit():
            if isinstance(command, int):
                if others is None:
                    return command
                else:
                    return 100
            elif isinstance(others, int):
                if isinstance(command, str):
                    return 100
                else:
                    return others
            else:
                return 100
        deleted = await ctx.channel.purge(limit=limit(), check=check, after=datetime.now()-timedelta(days=14))
        if len(deleted) >= 5:
            await ctx.send(f'**{len(deleted)} messages purged in {ctx.channel.mention}**')
    
    @commands.command()
    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    async def timeout(self, ctx, member: disnake.Member, _time: TimeoutConverter):
        """Add a timeout for a member"""
        if _time.days>7:
            await ctx.send("You can timeout members for max two hours")
        await member.timeout(duration=_time)
        await ctx.send(f"**{member} has been timed out for {_time}**")


def setup(Intensity):
    Intensity.add_cog(Moderation(Intensity))
