from __future__ import annotations

import uuid
from typing import Dict, List, Tuple, Set, Optional
import random
import asyncio

import discord
from discord.ext import commands, vbu


WORDLE_EMOJI_DICT = {
    "ALMOSTCORRECT": {
        "A": "<:ALMOSTCORRECT_A:933248989288079440>",
        "B": "<:ALMOSTCORRECT_B:933248989128699955>",
        "C": "<:ALMOSTCORRECT_C:933248989225177178>",
        "D": "<:ALMOSTCORRECT_D:933248989233553448>",
        "E": "<:ALMOSTCORRECT_E:933248989275500544>",
        "F": "<:ALMOSTCORRECT_F:933248989338423296>",
        "G": "<:ALMOSTCORRECT_G:933248989338402866>",
        "H": "<:ALMOSTCORRECT_H:933248989166465025>",
        "I": "<:ALMOSTCORRECT_I:933248989380362290>",
        "J": "<:ALMOSTCORRECT_J:933248989426491402>",
        "K": "<:ALMOSTCORRECT_K:933248989497790514>",
        "L": "<:ALMOSTCORRECT_L:933248989497798686>",
        "M": "<:ALMOSTCORRECT_M:933248989434880000>",
        "N": "<:ALMOSTCORRECT_N:933248989535543336>",
        "O": "<:ALMOSTCORRECT_O:933437642874433536>",
        "P": "<:ALMOSTCORRECT_P:933248989535535144>",
        "Q": "<:ALMOSTCORRECT_Q:933253558952951859>",
        "R": "<:ALMOSTCORRECT_R:933248989623640124>",
        "S": "<:ALMOSTCORRECT_S:933248989652987934>",
        "T": "<:ALMOSTCORRECT_T:933248989254541354>",
        "U": "<:ALMOSTCORRECT_U:933248989577502720>",
        "V": "<:ALMOSTCORRECT_V:933248989384556585>",
        "W": "<:ALMOSTCORRECT_W:933248989669777428>",
        "X": "<:ALMOSTCORRECT_X:933248989686554624>",
        "Y": "<:ALMOSTCORRECT_Y:933248989380362291>",
        "Z": "<:ALMOSTCORRECT_Z:933248989778837534>",
    },
    "CORRECT": {
        "A": "<:CORRECT_A:933249034334924810>",
        "B": "<:CORRECT_B:933249034389422131>",
        "D": "<:CORRECT_D:933249033798025216>",
        "R": "<:CORRECT_R:933249033835794473>",
        "F": "<:CORRECT_F:933249033852567592>",
        "E": "<:CORRECT_E:933249033860943882>",
        "G": "<:CORRECT_G:933249033869328444>",
        "C": "<:CORRECT_C:933249033881923614>",
        "J": "<:CORRECT_J:933249033886122014>",
        "I": "<:CORRECT_I:933249033894510612>",
        "X": "<:CORRECT_X:933249033902895115>",
        "H": "<:CORRECT_H:933249033902895144>",
        "K": "<:CORRECT_K:933249033932255232>",
        "L": "<:CORRECT_L:933249033936465930>",
        "Z": "<:CORRECT_Z:933249033936465933>",
        "M": "<:CORRECT_M:933249034045493258>",
        "N": "<:CORRECT_N:933249034049699860>",
        "P": "<:CORRECT_P:933249034062295070>",
        "O": "<:CORRECT_O:933249034066460744>",
        "S": "<:CORRECT_S:933249034129399808>",
        "T": "<:CORRECT_T:933249034171318332>",
        "U": "<:CORRECT_U:933249034204893204>",
        "W": "<:CORRECT_W:933249034217480212>",
        "V": "<:CORRECT_V:933249034280402974>",
        "Y": "<:CORRECT_Y:933249034427183104>",
        "Q": "<:CORRECT_Q:933253559254937630>",
    },
    "INCORRECT": {
        "G": "<:INCORRECT_G:933249165897633824>",
        "A": "<:INCORRECT_A:933249165989920819>",
        "B": "<:INCORRECT_B:933249166052827216>",
        "E": "<:INCORRECT_E:933249166115762186>",
        "D": "<:INCORRECT_D:933249166132531240>",
        "J": "<:INCORRECT_J:933249166132531241>",
        "H": "<:INCORRECT_H:933249166140919839>",
        "S": "<:INCORRECT_S:933249166153510973>",
        "F": "<:INCORRECT_F:933249166178676766>",
        "I": "<:INCORRECT_I:933249166212231168>",
        "C": "<:INCORRECT_C:933249166233202708>",
        "L": "<:INCORRECT_L:933249166233202709>",
        "P": "<:INCORRECT_P:933249166287732757>",
        "O": "<:INCORRECT_O:933249166329655376>",
        "M": "<:INCORRECT_M:933249166329671770>",
        "K": "<:INCORRECT_K:933249166333853786>",
        "N": "<:INCORRECT_N:933249166388371456>",
        "R": "<:INCORRECT_R:933249166392578068>",
        "T": "<:INCORRECT_T:933249166455492648>",
        "U": "<:INCORRECT_U:933249166505824287>",
        "X": "<:INCORRECT_X:933249166547759114>",
        "V": "<:INCORRECT_V:933249166602301470>",
        "Y": "<:INCORRECT_Y:933249166635847700>",
        "W": "<:INCORRECT_W:933249166661017660>",
        "Z": "<:INCORRECT_Z:933249166665203722>",
        "Q": "<:INCORRECT_Q:933253559229771796>",
        "BASE": "<:INCORRECT_BASE:933253559204585502>",
    }
}


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
        # if user.id == 141231597155385344:
        #     self.word = "POLAR"
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

        # If we're on a new system, return a button to spawn a modal
        return discord.ui.MessageComponents.add_buttons_with_rows(
            discord.ui.Button(label="Make guess", custom_id=f"{self.id} SPAWNMODAL", style=discord.ButtonStyle.primary)
        )

    def get_emoji_keyboard(self) -> str:
        """
        Get the keyboard of emoji guesses from the user.
        """

        letters = [
            "QWERTYUIOP",
            "ASDFGHJKL",
            "ZXCVBNM",
        ]
        guessed_letters = self.get_guessed_letters()
        letter_emojis = [[], [], []]
        for row_index, row in enumerate(letters):
            for letter in row:
                if letter in guessed_letters[0]:
                    letter_emojis[row_index].append(WORDLE_EMOJI_DICT["CORRECT"][letter])
                elif letter in guessed_letters[1]:
                    letter_emojis[row_index].append(WORDLE_EMOJI_DICT["INCORRECT"][letter])
                else:
                    letter_emojis[row_index].append(WORDLE_EMOJI_DICT["ALMOSTCORRECT"][letter])
        return "\n".join(["\u200b".join(i) for i in letter_emojis])

    def get_correct_guess(self) -> str:
        """
        Get the correctly guessed characters in one row.
        """

        correct_positions = [WORDLE_EMOJI_DICT["INCORRECT"]["BASE"]] * 5
        for g in self.guesses:
            for index, letter in enumerate(g):
                if self.word[index] == letter:
                    correct_positions[index] = WORDLE_EMOJI_DICT["CORRECT"][letter]
        return "\u200b".join(correct_positions)

    def get_emojis(self) -> str:
        """
        Get the list of emojis to be output as guesses.
        """

        output = []

        # Get a set of emojis for each of their guesses
        for guess in self.guesses:

            # Make a base string to build the emojis into
            line: List[Optional[str]] = [None] * len(guess)  # A list of guessed letter emojis
            word_list: List[Optional[str]] = list(self.word)  # A list of unguessed letters

            # See if they got it exactly right
            for index, letter in enumerate(guess):
                if word_list[index] == letter:
                    line[index] = WORDLE_EMOJI_DICT["CORRECT"][letter]
                    word_list[index] = None

            # See what they got in the wrong place
            for index, letter in enumerate(guess):
                if letter in word_list and line[index] is None:
                    line[index] = WORDLE_EMOJI_DICT["ALMOSTCORRECT"][letter]
                    word_list[word_list.index(letter)] = None

            # And for everything they got wrong entirely
            for index, letter in enumerate(guess):
                if line[index] is None:
                    line[index] = WORDLE_EMOJI_DICT["INCORRECT"][letter]

            # Add the emojis to our output list
            assert all(isinstance(i, str) for i in line)
            output.append("".join(line))  # type: ignore

        unguessed_guess = WORDLE_EMOJI_DICT['INCORRECT']['BASE']
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
        embed = discord.Embed().add_field(
            name="Keyboard",
            value=self.get_emoji_keyboard(),
            inline=False,
        ).add_field(
            name="Guess",
            value=self.get_correct_guess(),
            inline=False,
        )
        await interaction.response.send_message(
            content=self.get_emojis(),
            embed=embed,
            components=self.create_message_components(
                enter_enabled=False,
                backspace_enabled=False,
            ),
        )

        # Let's loop while they interact
        letter_buffer = []
        check = lambda i: i.custom_id.startswith(self.id) and i.user.id == self.user.id
        letter = ""
        while True:

            # Wait for an interaction
            done, pending = await asyncio.wait(
                [
                    self.bot.wait_for("component_interaction", check=check),
                    self.bot.wait_for("modal_submit", check=check),
                ],
                return_when=asyncio.FIRST_COMPLETED,
            )
            for p in pending:
                p.cancel()
            for d in done:
                interaction = d.result()

            # See what they clicked
            _, letter = interaction.custom_id.split(" ")
            if letter == "BACKSPACE":
                letter_buffer.pop()
            elif letter == "SUBMITMODAL":
                guessed_word = interaction.components[0].components[0].value.upper()
                if guessed_word not in self.bot.get_cog("WordleCommands").get_all_words():
                    await interaction.response.send_message(f"**{guessed_word}** isn't a valid word!", ephemeral=True)
                    continue
                self.guesses.append(guessed_word.upper())
                letter_buffer.clear()
                await interaction.response.defer_update()
                if self.guesses[-1] == self.word or len(self.guesses) == self.guess_count:
                    break
            elif letter == "SPAWNMODAL":
                await interaction.response.send_modal(
                    discord.ui.Modal(
                        title="Wordy Guess",
                        custom_id=f"{self.id} SUBMITMODAL",
                        components=[
                            discord.ui.ActionRow(
                                discord.ui.InputText(
                                    label="What is your guess?",
                                    custom_id=f"{self.id} INTPUTTEXT",
                                    min_length=5,
                                    max_length=5,
                                ),
                            ),
                        ],
                    ),
                )
                continue
            else:
                letter_buffer.append(letter)

            # Update the characters
            action = interaction.edit_original_message
            embed = discord.Embed().add_field(
                name="Keyboard",
                value=self.get_emoji_keyboard(),
                inline=False,
            ).add_field(
                name="Guess",
                value=self.get_correct_guess(),
                inline=False,
            )
            if letter_buffer:
                embed.title = "".join(letter_buffer)
            await action(
                content=self.get_emojis(),
                embed=embed,
                components=self.create_message_components(
                    enter_enabled=len(letter_buffer) == len(self.word),
                    backspace_enabled=len(letter_buffer) > 0,
                ),
            )

        # And done
        embed = None
        if self.guesses[-1] != self.word:
            embed = discord.Embed().add_field(name="Correct Word", value=self.word, inline=False)
        if letter == "SUBMITMODAL":
            action = interaction.edit_original_message
        else:
            action = interaction.response.edit_message
        await action(
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
