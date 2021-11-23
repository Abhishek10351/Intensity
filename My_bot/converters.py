from nextcord.ext.commands import Converter, CommandError
import re
from datetime import datetime , timedelta
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
                    minutes = argument
                    
                    return float(re.search(r"(\d+)", argument).group()) * 60
                elif argument.endswith(_hours):
                    hours = argument
                    return float(hours) * 3600
                elif re.search(argument, "|".join(_days)):
                    days = int(re.match(r"(^\d+)",argument).group())
                    return timedelta(days=days)
                elif argument.endswith(_weeks):
                    weeks = argument
                    return float(weeks) * 2592000
                elif argument.endswith(_months):
                    months = argument
                    return float(months) * 2592000
                elif argument.endswith(_years):
                    years = argument
                    return float(years) * 31104000
                elif argument.endswith(_seconds):
                    seconds = argument
                    return float(seconds)
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
        if argument in ['turnoff', 'off', '0', 'reset']:
            return 0
        else:
            if re.search("|".join(_minutes), argument):
                minutes = re.findall(r"^\d+", argument)[0]
                return timedelta(minutes=int(minutes))
            elif re.search("|".join(_hours), argument):
                hours = re.findall(r"^\d+", argument)[0]
                print(hours)
                return timedelta(hours=int(hours))
            elif re.search("|".join(_seconds), argument):
                seconds = re.findall(r"^\d+", argument)[0]
                return timedelta(seconds=int(seconds))
            else:
                raise ValueError

