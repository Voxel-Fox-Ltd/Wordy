from __future__ import annotations

import uuid
from typing import Dict, Iterable, List, Tuple, Set
import random
import json

import discord
from discord.ext import commands, vbu


WORDLE_EMOJIS = [
    ("ALMOSTCORRECT_B", "<:ALMOSTCORRECT_B:933248989128699955>"),
    ("ALMOSTCORRECT_H", "<:ALMOSTCORRECT_H:933248989166465025>"),
    ("ALMOSTCORRECT_C", "<:ALMOSTCORRECT_C:933248989225177178>"),
    ("ALMOSTCORRECT_D", "<:ALMOSTCORRECT_D:933248989233553448>"),
    ("ALMOSTCORRECT_T", "<:ALMOSTCORRECT_T:933248989254541354>"),
    ("ALMOSTCORRECT_E", "<:ALMOSTCORRECT_E:933248989275500544>"),
    ("ALMOSTCORRECT_A", "<:ALMOSTCORRECT_A:933248989288079440>"),
    ("ALMOSTCORRECT_G", "<:ALMOSTCORRECT_G:933248989338402866>"),
    ("ALMOSTCORRECT_F", "<:ALMOSTCORRECT_F:933248989338423296>"),
    ("ALMOSTCORRECT_I", "<:ALMOSTCORRECT_I:933248989380362290>"),
    ("ALMOSTCORRECT_Y", "<:ALMOSTCORRECT_Y:933248989380362291>"),
    ("ALMOSTCORRECT_V", "<:ALMOSTCORRECT_V:933248989384556585>"),
    ("ALMOSTCORRECT_J", "<:ALMOSTCORRECT_J:933248989426491402>"),
    ("ALMOSTCORRECT_M", "<:ALMOSTCORRECT_M:933248989434880000>"),
    ("ALMOSTCORRECT_O", "<:ALMOSTCORRECT_O:933437642874433536>"),
    ("ALMOSTCORRECT_K", "<:ALMOSTCORRECT_K:933248989497790514>"),
    ("ALMOSTCORRECT_L", "<:ALMOSTCORRECT_L:933248989497798686>"),
    ("ALMOSTCORRECT_P", "<:ALMOSTCORRECT_P:933248989535535144>"),
    ("ALMOSTCORRECT_N", "<:ALMOSTCORRECT_N:933248989535543336>"),
    ("ALMOSTCORRECT_U", "<:ALMOSTCORRECT_U:933248989577502720>"),
    ("ALMOSTCORRECT_R", "<:ALMOSTCORRECT_R:933248989623640124>"),
    ("ALMOSTCORRECT_S", "<:ALMOSTCORRECT_S:933248989652987934>"),
    ("ALMOSTCORRECT_W", "<:ALMOSTCORRECT_W:933248989669777428>"),
    ("ALMOSTCORRECT_X", "<:ALMOSTCORRECT_X:933248989686554624>"),
    ("ALMOSTCORRECT_Z", "<:ALMOSTCORRECT_Z:933248989778837534>"),
    ("CORRECT_D", "<:CORRECT_D:933249033798025216>"),
    ("CORRECT_R", "<:CORRECT_R:933249033835794473>"),
    ("CORRECT_F", "<:CORRECT_F:933249033852567592>"),
    ("CORRECT_E", "<:CORRECT_E:933249033860943882>"),
    ("CORRECT_G", "<:CORRECT_G:933249033869328444>"),
    ("CORRECT_C", "<:CORRECT_C:933249033881923614>"),
    ("CORRECT_J", "<:CORRECT_J:933249033886122014>"),
    ("CORRECT_I", "<:CORRECT_I:933249033894510612>"),
    ("CORRECT_X", "<:CORRECT_X:933249033902895115>"),
    ("CORRECT_H", "<:CORRECT_H:933249033902895144>"),
    ("CORRECT_K", "<:CORRECT_K:933249033932255232>"),
    ("CORRECT_L", "<:CORRECT_L:933249033936465930>"),
    ("CORRECT_Z", "<:CORRECT_Z:933249033936465933>"),
    ("CORRECT_M", "<:CORRECT_M:933249034045493258>"),
    ("CORRECT_N", "<:CORRECT_N:933249034049699860>"),
    ("CORRECT_P", "<:CORRECT_P:933249034062295070>"),
    ("CORRECT_O", "<:CORRECT_O:933249034066460744>"),
    ("CORRECT_S", "<:CORRECT_S:933249034129399808>"),
    ("CORRECT_T", "<:CORRECT_T:933249034171318332>"),
    ("CORRECT_U", "<:CORRECT_U:933249034204893204>"),
    ("CORRECT_W", "<:CORRECT_W:933249034217480212>"),
    ("CORRECT_V", "<:CORRECT_V:933249034280402974>"),
    ("CORRECT_A", "<:CORRECT_A:933249034334924810>"),
    ("CORRECT_B", "<:CORRECT_B:933249034389422131>"),
    ("CORRECT_Y", "<:CORRECT_Y:933249034427183104>"),
    ("INCORRECT_G", "<:INCORRECT_G:933249165897633824>"),
    ("INCORRECT_A", "<:INCORRECT_A:933249165989920819>"),
    ("INCORRECT_B", "<:INCORRECT_B:933249166052827216>"),
    ("INCORRECT_E", "<:INCORRECT_E:933249166115762186>"),
    ("INCORRECT_D", "<:INCORRECT_D:933249166132531240>"),
    ("INCORRECT_J", "<:INCORRECT_J:933249166132531241>"),
    ("INCORRECT_H", "<:INCORRECT_H:933249166140919839>"),
    ("INCORRECT_S", "<:INCORRECT_S:933249166153510973>"),
    ("INCORRECT_F", "<:INCORRECT_F:933249166178676766>"),
    ("INCORRECT_I", "<:INCORRECT_I:933249166212231168>"),
    ("INCORRECT_C", "<:INCORRECT_C:933249166233202708>"),
    ("INCORRECT_L", "<:INCORRECT_L:933249166233202709>"),
    ("INCORRECT_P", "<:INCORRECT_P:933249166287732757>"),
    ("INCORRECT_O", "<:INCORRECT_O:933249166329655376>"),
    ("INCORRECT_M", "<:INCORRECT_M:933249166329671770>"),
    ("INCORRECT_K", "<:INCORRECT_K:933249166333853786>"),
    ("INCORRECT_N", "<:INCORRECT_N:933249166388371456>"),
    ("INCORRECT_R", "<:INCORRECT_R:933249166392578068>"),
    ("INCORRECT_T", "<:INCORRECT_T:933249166455492648>"),
    ("INCORRECT_U", "<:INCORRECT_U:933249166505824287>"),
    ("INCORRECT_X", "<:INCORRECT_X:933249166547759114>"),
    ("INCORRECT_V", "<:INCORRECT_V:933249166602301470>"),
    ("INCORRECT_Y", "<:INCORRECT_Y:933249166635847700>"),
    ("INCORRECT_W", "<:INCORRECT_W:933249166661017660>"),
    ("INCORRECT_Z", "<:INCORRECT_Z:933249166665203722>"),
    ("INCORRECT_BASE", "<:INCORRECT_BASE:933253559204585502>"),
]


class WordleGame:

    bot: vbu.Bot
    GAMES: Dict[str, WordleGame] = {}

    CORRECT_GUESS = "\N{LARGE GREEN SQUARE}"
    INCRRECT_GUESS = "\N{BLACK LARGE SQUARE}"
    ALMOSTCORRECT_GUESS = "\N{LARGE YELLOW SQUARE}"
    UNGUESSED_GUESS = "\N{WHITE SQUARE BUTTON}"

    def __init__(self, *, user: discord.User | discord.Member, word: str, guess_count: int):
        self.id: str = str(uuid.uuid4())
        self.user = user
        self.word = word.upper()
        self.guess_count = guess_count
        self.guesses: List[str] = []

    def create_message_components(
            self: WordleGame,
            *,
            enter_enabled: bool = True,
            backspace_enabled: bool = False,
            ) -> discord.ui.MessageComponents:
        """
        Create a keyboard to use in a Wordle game.
        """

        letters = [
            "ABCDE",
            "FGHIK",
            "LMNOP",
            "RSTUV",
            "WXY",
        ]  # ZJQ are removed
        guessed_letters = self.get_guessed_letters()
        v = discord.ui.MessageComponents(*[
            discord.ui.ActionRow(*[
                discord.ui.Button(
                    label=l,
                    custom_id=f"{self.id} {l}",
                    disabled=enter_enabled,
                    style=discord.ButtonStyle.green if l in guessed_letters[0] else discord.ButtonStyle.grey if l in guessed_letters[1] else discord.ButtonStyle.blurple,
                )
                for l in i
            ])
            for i in letters
        ])
        v.components[-1].components.extend([
            discord.ui.Button(
                label="Enter",
                custom_id=f"{self.id} ENTER",
                style=discord.ButtonStyle.success,
                disabled=not enter_enabled,
            ),
            discord.ui.Button(
                label="<-",
                custom_id=f"{self.id} BACKSPACE",
                style=discord.ButtonStyle.danger,
                disabled=not backspace_enabled,
            ),
        ])
        return v

    def get_emojis(self) -> str:
        """
        Get the emoji list for the bullshit.
        """

        output = []

        for guess in self.guesses:
            line = ""
            for index, letter in enumerate(guess):
                if letter == self.word[index]:
                    line += [o for i, o in WORDLE_EMOJIS if i.startswith("CORRECT") and i.endswith(f"_{letter}")][0]
                elif letter in self.word:
                    line += [o for i, o in WORDLE_EMOJIS if i.startswith("ALMOSTCORRECT") and i.endswith(f"_{letter}")][0]
                else:
                    line += [o for i, o in WORDLE_EMOJIS if i.startswith("INCORRECT") and i.endswith(f"_{letter}")][0]
            output.append(line)

        unguessed_guess = [o for i, o in WORDLE_EMOJIS if i == "INCORRECT_BASE"][0]
        while len(output) < self.guess_count:
            output.append(unguessed_guess * len(self.word))
        return "\n".join(output)

    def get_guessed_letters(self) -> Tuple[str, str]:
        """
        Get the letters that the user has guessed correctly and incorrectly.
        """

        correct: Set[str] = set()
        incorrect: Set[str] = set()
        for g in self.guesses:
            for l in g:
                if l in self.word:
                    correct.add(l)
                else:
                    incorrect.add(l)
        return "".join(tuple(correct)), "".join(tuple(incorrect))

    async def start(self, interaction: discord.Interaction):
        """
        Run the Wordle game handler.
        """

        # Send the initial message
        await interaction.response.send_message(
            content=self.get_emojis(),
            components=self.create_message_components(
                enter_enabled=False,
                backspace_enabled=False,
            ),
        )

        # Let's loop while they interact
        letter_buffer = []
        while True:

            # Wait for an interaction
            interaction = await self.bot.wait_for(
                "component_interaction",
                check=lambda i: i.custom_id.startswith(self.id) and i.user.id == self.user.id
            )

            # See what they clicked
            _, letter = interaction.custom_id.split(" ")
            if letter == "BACKSPACE":
                letter_buffer.pop()
            elif letter == "ENTER":
                guessed_word = "".join(letter_buffer)
                if guessed_word not in self.bot.get_cog("WordleCommands").get_all_words():
                    await interaction.response.send_message(f"**{guessed_word}** isn't a valid word!", ephemeral=True)
                    continue
                self.guesses.append(guessed_word)
                letter_buffer.clear()
                if self.guesses[-1] == self.word or len(self.guesses) == self.guess_count:
                    break
            else:
                letter_buffer.append(letter)

            # Update the characters
            await interaction.response.edit_message(
                content=self.get_emojis(),
                embed=discord.Embed(title="".join(letter_buffer)) if letter_buffer else None,
                components=self.create_message_components(
                    enter_enabled=len(letter_buffer) == len(self.word),
                    backspace_enabled=len(letter_buffer) > 0,
                ),
            )

        # And done
        embed = None
        if self.guesses[-1] != self.word:
            embed = discord.Embed().add_field(name="Correct Word", value=self.word, inline=False)
        await interaction.response.edit_message(
            content=self.get_emojis(),
            embed=embed,
            components=None,
        )


class WordleCommands(vbu.Cog[vbu.Bot]):

    def __init__(self, bot: vbu.Bot):
        super().__init__(bot)
        self._keywords = None
        self._all_words = None
        self.get_words()
        self.get_all_words()

    def get_words(self) -> Tuple[str]:
        """
        Get a list of every word in the English language.
        """

        # Only get them once
        if self._keywords is not None:
            return self._keywords

        # Get from local files
        with open("new_words.txt") as a:
            text = a.read()
        self._keywords = tuple(i.strip().upper() for i in text.strip().split("\n") if len(i.strip()) == 5)
        return self._keywords

    def get_all_words(self) -> Tuple[str]:
        """
        Get a list of every word in the English language.
        """

        # Only get them once
        if self._all_words is not None:
            return self._all_words

        # Get from local files
        with open("words_alpha.txt") as a:
            text = a.read()
        self._all_words = tuple(i.strip().upper() for i in text.strip().split("\n") if len(i.strip()) == 5)
        return self._all_words

    @commands.command(
        application_command_meta=commands.ApplicationCommandMeta(),
    )
    async def wordle(self, ctx: vbu.SlashContext, characters: int = 5, guesses: int = None):
        """
        A classic game of wordle.
        """

        # Make sure we have a valid number of guesses
        if guesses is None:
            guesses = characters + 1

        # Make sure all of our numbers are valid
        if characters < 2:
            return await ctx.interaction.response.send_message("You can't give fewer than two characters.")
        if guesses < 1:
            return await ctx.interaction.response.send_message("You can't give fewer than two guesses.")

        # Pick a word for them to have to guess
        all_words = self.get_words()
        valid_words = [i for i in all_words if len(i) == characters and not any(c in "ZJQ" for c in i)]
        picked_word = random.choice(valid_words)

        # And it's game time
        assert ctx.author
        game = WordleGame(user=ctx.author, word=picked_word, guess_count=guesses)
        await game.start(ctx.interaction)


def setup(bot: vbu.Bot):
    WordleGame.bot = bot
    x = WordleCommands(bot)
    bot.add_cog(x)
