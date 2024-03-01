import disnake
from disnake.ext import commands


class VotingSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_votes = {}  # Słownik do przechowywania aktywnych głosowań
        self.voted_users = {}  # Słownik do przechowywania informacji o użytkownikach, którzy oddali swoje głosy

    @commands.slash_command(name="ankieta")
    async def vote(self, inter):
        pass
    @vote.sub_command(name="stwórz", description="Rozpocznij ankietę")
    async def startvote(self, inter, question: str, answers: str = ""):
        """Rozpocznij nowe głosowanie"""
        if inter.channel_id in self.active_votes:
            await inter.response.send_message("W tym kanale jest już aktywna ankieta!")
            return

        if not answers:
            await inter.response.send_message("Musisz podać co najmniej jedną opcję odpowiedzi.")
            return

        answers_list = answers.split(", ")
        if len(answers_list) > 5:
            await inter.response.send_message("Proszę podać maksymalnie 5 odpowiedzi.")
            return

        # Inicjalizacja śledzenia głosowania
        self.active_votes[inter.channel_id] = {answer: 0 for answer in answers_list}

        embed = disnake.Embed(title="Ankieta", description=question)
        embed.set_footer(text=f"Ankieta zainicjowana przez {inter.author.display_name}")

        # Tworzenie przycisków dla każdej opcji
        components = [[
            disnake.ui.Button(style=disnake.ButtonStyle.primary,
                              label=f"{answer}",
                              custom_id=f"{answer}_{inter.channel_id}") for answer in answers_list
        ]]

        message = await inter.response.send_message(embed=embed, components=components)
        self.active_votes[inter.channel_id]["message"] = message

    @commands.Cog.listener()
    async def on_button_click(self, inter):
        # Sprawdzenie, czy kliknięcie dotyczy aktywnego głosowania
        if inter.message.id not in [msg.id for msg in await inter.channel.history(limit=200).flatten()]:
            return

        user_id = inter.user.id
        vote = inter.component.custom_id
        vote_option, channel_id = vote.split("_")

        if user_id in self.voted_users.get(int(channel_id), []):
            await inter.response.send_message("Już oddałeś(-aś) swój głos w tej ankiecie !", ephemeral=True)
            return

        if channel_id == str(inter.channel_id):
            if vote_option in self.active_votes.get(int(channel_id), {}):
                self.active_votes[int(channel_id)][vote_option] += 1
                self.voted_users.setdefault(int(channel_id), []).append(user_id)
                await inter.response.send_message(f"Twój głos na '{vote_option}' został policzony.", ephemeral=True)

    @vote.sub_command(name="zakończ", description="Zakończ obecną ankietę.")
    async def endvote(self, inter):
        """Zakończ obecne głosowanie i wyświetl wyniki"""
        if inter.channel_id not in self.active_votes:
            await inter.response.send_message("W tym kanale nie ma aktywnej ankiety.")
            return

        # Check if the vote has already ended
        if "message" not in self.active_votes[inter.channel_id]:
            await inter.response.send_message("Ta ankieta została zakończona.")
            return

        # Sprawdź, czy istnieją jakiekolwiek głosy
        votes = self.active_votes.get(inter.channel_id, {})
        if not any(votes.values()):
            await inter.response.send_message("Nie ma żadnych głosów w tej ankiecie.")
            return

        # Znajdź opcję z największą liczbą głosów
        non_none_votes = {k: v for k, v in votes.items() if v is not None}
        if not non_none_votes:
            await inter.response.send_message("Wystąpił błąd podczas przetwarzania głosów. Proszę spróbować ponownie.")
            return

        winner_option = max(non_none_votes, key=non_none_votes.get)

        embed = disnake.Embed(title="Wyniki ankiety", description=f"Opcja z największą ilością głosów: {winner_option}")
        for answer, count in non_none_votes.items():
            embed.add_field(name=answer, value=str(count), inline=False)

        # Send the voting results as a new message
        await inter.response.send_message(embed=embed, ephemeral=True)

        # Remove the active vote data
        del self.active_votes[inter.channel_id]
        del self.voted_users[inter.channel_id]


def setup(bot):
    bot.add_cog(VotingSystem(bot))
