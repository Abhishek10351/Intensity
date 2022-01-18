from disnake.ext.commands import Converter, CommandError
import re
from datetime import datetime, timedelta
from random import randint
"""Module for Converting user input into their respective types"""


class TimeConverter(Converter):
    async def convert(self, ctx, argument: str):
        numbers = tuple([map(str, range(10))])
        _seconds = ('seconds', 'second', 'sec', 's')
        _minutes = ('minutes', 'minute', 'min', 'm')
        _hours = ('hours', 'hour', "hr", 'h')
        _days = ('days', 'day', 'd')
        _weeks = ('weeks', 'week', 'w')
        _months = ('months', 'month')
        _years = ('years', 'year', 'y')
        if re.match(r"^\d+\D{1,7}", argument):
            try:
                if argument.endswith(_minutes):
                    minutes = float(re.search(r"(\d+)", argument).group())
                    return timedelta(minutes=minutes)
                elif argument.endswith(_hours):
                    hours = int(re.match(r"(^\d+)", argument).group())
                    return timedelta(hours=hours)
                elif re.search(argument, "|".join(_days)):
                    days = int(re.match(r"(^\d+)", argument).group())
                    return timedelta(days=days)
                elif argument.endswith(_weeks):
                    weeks = int(re.match(r"(^\d+)", argument).group())
                    return timedelta(weeks=weeks)
                elif argument.endswith(_months):
                    months = int(re.match(r"(^\d+)", argument).group())
                    return timedelta(days=days*30)
                elif argument.endswith(_years):
                    years = int(re.match(r"(^\d+)", argument).group())
                    return timedelta(days=years*365)
                elif argument.endswith(_seconds):
                    seconds = int(re.match(r"(^\d+)", argument).group())
                    return timedelta(seconds=seconds)
                else:
                    return None
            except Exception as e:
                print(str(e))
            # else:
                #   return None
        else:
            raise ConversionError


class SlowmodeTimeConverter(Converter):

    async def convert(self, ctx, argument: str):
        argument = argument.lower()
        _seconds = ('seconds', 'second', 'sec', 's')
        _minutes = ('minutes', 'minute', 'min', 'm')
        _hours = ('hours', 'hour', 'hr', 'h')
        if re.search("|".join(_minutes), argument):
            minutes = re.findall(r"^\d+", argument)[0]
            return timedelta(minutes=int(minutes))
        elif re.search("|".join(_hours), argument):
            hours = re.findall(r"^\d+", argument)[0]
            return timedelta(hours=int(hours))
        elif re.search("|".join(_seconds), argument):
            seconds = re.findall(r"^\d+", argument)[0]
            return timedelta(seconds=int(seconds))
        else:
            return None
