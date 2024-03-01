import disnake
from disnake.ext import commands
import random
import asyncio


class RollADice(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="rzutkostka", description="Rzuca kostka i losuje liczbe od 1 do 6")
    async def rzutkostka(self, inter: disnake.ApplicationCommandInteraction):
        embed = disnake.Embed(
            description=f"🎲 Wylosowales liczbe: {random.randint(1, 6)}",
            color=6697881
        )
        embed.set_footer(text=f"{inter.user.name} rzucił kostką!")
        await inter.response.send_message(embed=embed)


class ReverseText(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(description='Odwraca podany tekst.')
    async def reverse(self, inter, text: str):
        if len(text) > 50:
            await inter.response.send_message('Twój tekst jest za długi! Ponieważ zawiera powyżej 50 znaków.',
                                              ephemeral=True)
        else:
            reversed_text = text[::-1]
            embed = disnake.Embed(
                title="Odwrócony tekst",
                description=f"Odwrócony tekst: {reversed_text}",
                color=6697881
            )
            embed.set_footer(text=f"{inter.user.name} wykonał polecenie /reverse")
            await inter.response.send_message(embed=embed)


class Reminder(commands.Cog):
    @commands.slash_command(name="minutnik", description="Ustawia minutnik")
    async def timer(inter: disnake.ApplicationCommandInteraction, seconds: int):
        if len(str(seconds)) > 5:
            await inter.response.send_message(f"Podałeś zbyt długi czas!", ephemeral=True)
        else:
            reminderembed = disnake.Embed(
                title="⏰ Minutnik",
                description=f"Ustawiam minutnik dla użytkownika {inter.author.mention} na {seconds} sekund.",
                color=6697881
            )
            await inter.response.send_message(embed=reminderembed)
            await asyncio.sleep(seconds)
            endembed = disnake.Embed(
                title="⏲ Minutnik wygasł",
                description=f"{inter.author.mention}, twój minutnik wygasł!",
                color=6697881
            )
            endembed.set_footer(text=f"{inter.user.name}")
            await inter.followup.send(embed=endembed)


class TicTacToe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = {}

    async def draw_board(self, ctx, board):
        board_str = ""
        for row in board:
            board_str += " ".join(row) + "\n"
        await ctx.send(board_str)

    @commands.slash_command(name="kolkoikrzyzyk", description="Wyzwij kogos na pojedynek!")
    async def kolkoikrzyzyk(self, ctx, przeciwnik: disnake.Member = None):
        author = ctx.author

        if przeciwnik is None:
            await ctx.send("Kogo chcesz wyzwac na pojedynek?")
            return

        if przeciwnik == author:
            await ctx.send("Nie możesz zagrać przeciwko sobie.")
            return

        if ctx.channel.id in self.games:
            await ctx.send("Jest już nie skonczona gra na tym kanale.")
            return

        self.games[ctx.channel.id] = {
            "author": author,
            "opponent": przeciwnik,
            "turn": author,
            "board": [["⬜️", "⬜️", "⬜️"] for _ in range(3)],
        }

        await self.draw_board(ctx, self.games[ctx.channel.id]["board"])
        await ctx.send(f"{author.mention} rozpoczyna pierwszy. Użyj `/ruch rząd kolumna` aby wykonać ruch.")

    @commands.slash_command(name="ruchwkik", description="Użyj aby poruszyć się w kółko i krzyżyk!",
                            help="row = rząd, column = kolumna")
    async def ruch(self, ctx, row: int, column: int):
        if ctx.channel.id not in self.games:
            await ctx.send("Nie ma gry na tym kanale. Rozpocznij jedną używając `/kolkoikrzyzyk`.")
            return

        game = self.games[ctx.channel.id]

        if ctx.author != game["turn"]:
            await ctx.send("Nie jest twoja kolej.")
            return

        # Adjust indices to be zero-based
        row -= 1
        column -= 1

        if not (0 <= row < 3) or not (0 <= column < 3):
            await ctx.send(
                "Nieprawidłowy ruch. Użyj `/ruch rząd kolumna` gdzie rząd i kolumna są numerami pomiędzy 1 a 3.")
            return

        if game["board"][row][column] != "⬜️":
            await ctx.send("Nieprawidłowy ruch. To miejsce jest już zajęte!.")
            return

        marker = "❌" if ctx.author == game["author"] else "⭕"
        game["board"][row][column] = marker

        await self.draw_board(ctx, game["board"])

        if self.check_winner(game["board"], marker):
            await ctx.send(f"{ctx.author.mention} wygrywa!")
            del self.games[ctx.channel.id]
        elif self.is_board_full(game["board"]):
            await ctx.send("Jest remis!")
            del self.games[ctx.channel.id]
        else:
            game["turn"] = game["opponent"] if ctx.author == game["author"] else game["author"]
            await ctx.send(f"{game['turn'].mention} twoja kolej.")

    @commands.slash_command(name="zakończkik", description="Zakończ bieżącą grę w kółko i krzyżyk.")
    async def zakonczrozgrywkekik(self, ctx):
        if ctx.channel.id not in self.games:
            await ctx.send("Nie ma bieżącej gry na tym kanale.")
            return

        del self.games[ctx.channel.id]
        await ctx.send("Rozgrywka została zakończona.")

    def check_winner(self, board, marker):
        # Check rows, columns, and diagonals
        for i in range(3):
            if all(cell == marker for cell in board[i]) or all(board[j][i] == marker for j in range(3)):
                return True
        if all(board[i][i] == marker for i in range(3)) or all(board[i][2 - i] == marker for i in range(3)):
            return True
        return False

    def is_board_full(self, board):
        return all(cell != "⬜️" for row in board for cell in row)


class Emotions(commands.Cog):
    @commands.slash_command(name="przytul", description="Przytula wybranego użytkownika!")
    async def hug(self, inter, user: disnake.User = None):
        if user is None:
            await inter.response.send_message("Musisz podać użytkownika, którego chcesz przytulić!")
            return
        gif_urls_hug = [
            'https://media1.tenor.com/m/TO3XZieplToAAAAd/cat-kiss-cock.gif',
            'https://media1.tenor.com/m/m0DnmklkzAEAAAAd/allex-ano.gif',
            'https://media1.tenor.com/m/DRgXad_JuuQAAAAC/bobitos-mimis.gif',
            'https://media.tenor.com/YFYtOlJWYbUAAAAi/love-couple.gif',
            'https://media1.tenor.com/m/eAKshP8ZYWAAAAAC/cat-love.gif',
            'https://media1.tenor.com/m/Eqyc77UPQFkAAAAd/cats-hugs.gif',
            'https://media1.tenor.com/m/-taxDgyC6AMAAAAd/holaroberto3.gif',
            'https://media1.tenor.com/m/PCJUrAADbR0AAAAd/cat-love.gif',
            'https://media1.tenor.com/m/h3g40mXXhuUAAAAC/excited.gif',
        ]
        selected_gif_hug = random.choice(gif_urls_hug)
        embed = disnake.Embed(
            description=f"{inter.author.name} przytula {user.mention} 💕!",
            color=16761035
        )
        embed.set_image(url=selected_gif_hug)
        await inter.response.send_message(embed=embed)

    @commands.slash_command(name="pocaluj", description="Całuje wybranego użytkownika!")
    async def kiss(self, inter, user: disnake.User = None):
        if user is None:
            await inter.response.send_message("Musisz podać użytkownika, którego chcesz pocałować!")
            return
        gif_urls_kiss = [
            'https://media1.tenor.com/m/gxF2wutqCdsAAAAC/cat-cute.gif',
            'https://media1.tenor.com/m/ieLjKXbfy-AAAAAd/barbanne-canele.gif',
            'https://media1.tenor.com/m/R8PxtpOChNcAAAAd/kitty-kiss-kitty.gif',
            'https://media1.tenor.com/m/PNNHoG-7zuMAAAAC/peach-and.gif',
            'https://media1.tenor.com/m/iGOU08nTk_sAAAAd/cat-kiss-alydn.gif',
            'https://media1.tenor.com/m/XeqEa0peiIYAAAAC/kitty-kiss-kitties-kissing.gif',
            'https://media1.tenor.com/m/UZMDKcNeUj0AAAAC/goma-peach-kisses.gif',
            'https://media1.tenor.com/m/5Uf-QGpf6GMAAAAd/kiss-love.gif',
        ]
        selected_gif_kiss = random.choice(gif_urls_kiss)
        embed = disnake.Embed(
            description=f"{inter.author.name} całuje {user.mention} 😽!",
            color=16761035
        )
        embed.set_image(url=selected_gif_kiss)
        await inter.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(RollADice(bot))
    bot.add_cog(ReverseText(bot))
    bot.add_cog(Reminder(bot))
    bot.add_cog(TicTacToe(bot))
    bot.add_cog(Emotions(bot))
