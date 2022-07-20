from disnake import ui, ButtonStyle, Interaction
from typing import List


class Confirm(ui.View):
    def __init__(self, members: List):
        super().__init__()
        self.value = None

    @ui.button(label='Confirm', style=ButtonStyle.green)
    async def confirm(self, button: ui.Button, interaction: Interaction):
        self.value = True
        for i in children:
            i.disabled = True
        await interaction.response.edit_message(content="Confirmed", ephemeral=True)

    @ui.button(label='Cancel', style=ButtonStyle.grey)
    async def cancel(self, button: ui.Button, interaction: Interaction):
        self.value = False
        for i in children:
            i.disabled = True
        await interaction.response.edit_message(content="Cancelled", ephemeral=True)

    async def interaction_check(self, interaction):
        if interaction.user not in members:
            await interaction.response.send_message("https://tenor.com/view/rick-roll-rick-ashley-never-gonna-give-you-up-gif-22113173", ephemeral=True)
            return False
        else:
            return True


class TicTacToeButtons(ui.Button):
    def __init__(self, row: int, index: int):
        self.row = row
        self.index = index
        self.value = index
        super().__init__(style=ButtonStyle.secondary, label='\u200b', row=row)

    async def callback(self, interaction: Interaction):
        view: TicTacToeGame = self.view
        if interaction.user == view.current_game[0]:
            self.emoji = view.current_game[1]
            self.style = view.current_game[2]
            self.disabled = True

            view.board[self.index] = view.current_game[1]
            if view.check_win(view.board):
                for button in view.children:
                    button.disabled = True
                await interaction.response.edit_message(content=f"Yay {view.current_game[0].mention} u won <a:vibindoggo:779631210249977866>", view=view)
                return
            elif view.is_final():
                await interaction.response.edit_message(content=f"It's a draw <a:pepeboom:858958157698826260>", view=view)
                return
            view.current_game = next(view.game)
            await interaction.response.edit_message(content=f"It's your turn {view.current_game[0].mention}", view=view)

        else:
            await interaction.response.send_message("It's not your turn :grimacing:", ephemeral=True)


class TicTacToeGame(ui.View):
    children: List[TicTacToeButtons]

    def __init__(self, game, current_game):
        self.game = game
        super().__init__(timeout=180)
        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButtons(y, (x*3)+y))
        self.board = "1️⃣ 2️⃣ 3️⃣ 4️⃣ 5️⃣ 6️⃣ 7️⃣ 8️⃣ 9️⃣".split(" ")
        self.current_game = current_game

    def check_win(self, current_board):
        """checks if any user won the game"""
        board = current_board
        return any((  # Horizontal
            (board[0] == board[1] == board[2]),
            (board[3] == board[4] == board[5]),
            (board[6] == board[7] == board[8]),
            # Vertical
            (board[0] == board[3] == board[6]),
            (board[1] == board[4] == board[7]),
            (board[2] == board[5] == board[8]),
            # Diagonal
            (board[0] == board[4] == board[8]),
            (board[2] == board[4] == board[6]),
        ))

    def is_final(self):
        """Checks if the current choice is the final choice"""
        return (self.board.count("<:ttt_x:902516406090878976>") + self.board.count("<:ttt_y:902515608640434198>")) == 9


class RPSButtons(ui.Button):
    def __init__(self, emote, val):
        self.emote = emote
        self.value = val
        super().__init__(emoji=emote, style=ButtonStyle.grey)

    async def callback(self, interaction: Interaction):
        view = self.view
        if view.game[interaction.user] is None:
            view.game[interaction.user] = self.value
            if None in view.game.values():
                await interaction.response.edit_message(content=f"**{interaction.user} has made their move**", view=view)
                return
            else:
                ac = view.game[view.player]
                pc = view.game[view.opponent]
                val = view.WINNER_DICT[ac][pc]

                for i in view.children:
                    i.disabled = True

                if val == 0:
                    await interaction.response.edit_message(content="**It's a draw**", view=view)
                    return
                elif val == 1:
                    await interaction.response.edit_message(content=f"**{view.player} Won by chosing {ac}**", view=view)
                    return
                elif val == -1:
                    await interaction.response.edit_message(content=f"**{view.opponent} Won by chosing {pc}**", view=view)
                    return
            await interaction.response.edit_message(content=f"**{interaction.user} has chosen**", view=view)
        else:
            await interaction.response.send_message(":grimacing: you already selected", ephemeral=True)


class RPSGames(ui.View):
    def __init__(self, player, opponent):
        self.player = player
        self.opponent = opponent
        super().__init__()
        emojis = ["<:Rock:909069636060999690>",
                  "<:Paper:909069634324533280>", "<:Scissors:909069637331873802>"]
        for emoji, value in zip(emojis, ["r", "p", "s"]):
            self.add_item(RPSButtons(emote=emoji, val=value))
        self.game = {}
        self.game[player] = None
        self.game[opponent] = None
        self.WINNER_DICT = {
            "r": {
                "r": 0,
                "p": -1,
                "s": 1,
            },
            "p": {
                "r": 1,
                "p": 0,
                "s": -1,
            },
            "s": {
                "r": -1,
                "p": 1,
                "s": 0,
            }
        }

    async def interaction_check(self, interaction):
        if interaction.user not in [self.player, self.opponent]:
            await interaction.response.send_message("https://tenor.com/view/rick-roll-rick-ashley-never-gonna-give-you-up-gif-22113173", ephemeral=True)
            return False
        else:
            return True


class Paginator(ui.View):
    def __init__(self):
        self.value = 0
        super().__init__()
    
    @ui.button(emoji="👉")
    async def right(self, button, interaction):
        self.value += 1
        await interaction.response.edit_message(content=self.value)
    @ui.button(emoji="👈")
    async def left(self, button, interaction):
        self.value -= 1
        await interaction.response.edit_message(content=self.value)