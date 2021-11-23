from nextcord import Embed, Colour
from nextcord.ext.commands import HelpCommand
class CustomHelpCommand(HelpCommand):
    async def send_bot_help(self, mapping):
        """Sends information about the bot"""
        embed = Embed(
            description='```yaml\nAvailable Modules for Intensity\n```', color=Colour.random())
        for cog in mapping:
            if cog is not None and cog.qualified_name not in ['Reply', 'Status']:
                embed.add_field(
                    name=cog.qualified_name, value=f'**{", ".join([command.name for command in mapping[cog]])}**')
        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog):
        """Sends information about the given Module"""
        embed = Embed(
            description=f'```yaml\n{cog.qualified_name}:\n{cog.description}```', color=Colour.random())
        embed.add_field(name="**Available commands**",
                        value=f'**{", ".join([command.name for command in cog.__cog_commands__])}**')
        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command):
        """ Sends information about the given command."""
        embed = Embed(title=command, description=f'**{command.help}**',
                               color=Colour.random())
        if command.aliases:
            embed.add_field(name="Command Aliases", value=f'**{ ", ".join(command.aliases)}**')
        await self.get_destination().send(embed=embed)
    
    async def send_group_help(self, group):
        embed = Embed(title=group,description=f"**{group.short_doc}**", color=Colour.random())
        await self.get_destination().send(embed=embed)

