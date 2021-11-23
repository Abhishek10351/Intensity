import nextcord
from nextcord.ext import commands
from pandas import DataFrame, read_csv
from random import randint, choice
from numpy import int64
from emojis import no
import asyncio
from typing import Union, Optional
from randfacts import get_fact
from urllib.parse import urljoin

class Fun(commands.Cog):
    def __init__(self, Intensity: commands.Bot):
        self.Intensity = Intensity

    @commands.command(name='pokemon', aliases=('pokedex', 'pokémon', 'pokédex'))
    #@cooldown(1, 10, commands.BucketType.user)
    @commands.guild_only()
    async def pokemon(self, ctx, id_name: Union[int, str]=None, *, form=''):
        """ Sends details about the given pokemon according to name or ID.
        Sends info of a random pokemon if no name/id is given """
        await ctx.trigger_typing()
        info = read_csv(r'G:\Hello_Python\Python\Pokemon\Pokemon.csv')
        names = list(info['Name'])
        emoji = choice(no)
        form = form.lower().title()
        if id_name is None:
            id = randint(1, 898)
            info = info.set_index("ID", drop=False)
            poke_info = info.loc[id]
        elif isinstance(id_name, int):
            id = int(id_name)
            if id not in range(1, 899):
                await ctx.message.add_reaction(emoji)
                await ctx.reply(f'**Pokémon with the Id: {id_name} not found.\nEnter a value between 1-898.**')
                return
            elif id in range(1, 899):
                info = info.set_index("ID", drop=False)
                poke_info = info.loc[id]
        else:
            if id_name.title() not in list(info["Name"]):
                await ctx.message.add_reaction(emoji)
                await ctx.reply(f'**Pokémon with the Name: {id_name} not found.\nEnter a valid Name.**')
                return
            elif id_name.title() in names:
                info = info.set_index("Name", drop=False)
                name = id_name.replace('  ', ' ')
                poke_info = info.loc[name]
                id = poke_info['ID']
                if isinstance(id, int64):
                    id = int(id)
                if not isinstance(id, int):
                    id = id[0]

        forms = list(poke_info.T.loc['Form'])
        try:
            if isinstance(poke_info, DataFrame):
                if not form:
                    poke_info = poke_info.iloc[0]
                elif form.replace(' ', '').isalpha():
                    try:
                        poke_info = poke_info.set_index('Form')
                        poke_info = poke_info.loc[form]
                    except KeyError:
                        await ctx.send(embed=nextcord.Embed(description=f'{poke_info.iloc[1]} has no form {form}'))
                        return
            name = poke_info.iloc[1]
            forms = [i for i in forms if i != ' ']
            forms = ', '.join(forms)
            _type = poke_info.iloc[3]
            if not str(poke_info.iloc[4]).isspace():
                _type += f', {poke_info.iloc[4]}'
            gen = poke_info.iloc[-1]
            regions = 'Kanto Johto Hoenn Sinnoh Unova Kalos Alola Galar'.split()
            region = regions[gen - 1]
            hp = poke_info.iloc[6]
            attack = poke_info.iloc[7]
            defense = poke_info.iloc[8]
            speed = poke_info.iloc[-2]
            details = f'**Form: {form}\nTypes: {_type}\nHp: {hp}\nAttack: {attack}\nDefense: {defense}\nSpeed: {speed}\n'
            details += f'Generation: {gen}\nRegion: {region}'
            if len(forms) > 1:
                details += f'\nForms: {forms}'
            details += '**'
            url = f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{id}.png'
            user_name = f'{ctx.author}'
            embed = nextcord.Embed(
                title=f"#{id}-{name}", description=details, color=0Xffff)
            embed.set_thumbnail(url=url)
            if not id_name:
                embed.set_author(
                    name=f'{ctx.author.display_name}\'s random pokemon', icon_url=ctx.author.avatar_url)
            else:
                embed.set_author(
                    name=f'Invoked by {user_name}', icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            _link = f'http://play.pokemonshowdown.com/sprites/ani/{name.lower().replace(" ", "").replace(".", "")}.gif'
            # await ctx.send(_link)
        except UnboundLocalError:
            pass

    @commands.command(name='tts', aliases=['say'])
    @commands.guild_only()
    @commands.has_permissions(send_tts_messages=True)
    @commands.bot_has_permissions(send_tts_messages=True)
    async def tts(self, ctx, *, message=None):
        """Converts your text message to `text to speech` message """
        if message is not None:
            await ctx.send(message, tts=True)
        else:
            await ctx.send('**Idiot enter something to covert to tts**')

    @commands.command(aliases=['fact', 'facts'])
    @commands.guild_only()
    async def randfact(self, ctx, type: Optional[str] = None):
        """Get a random fact"""
        fact = get_fact()
        embed = nextcord.Embed(
            description=f'**{fact}**', colour=nextcord.Color.random())
        await ctx.send(embed=embed)
    
    


def setup(Intensity):
    Intensity.add_cog(Fun(Intensity))
