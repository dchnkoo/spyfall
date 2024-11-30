from aiogram.client.bot import BotCommand


class Commands:
    def __iter__(self):
        for command in self.__dir__():
            if isinstance((obj := getattr(self, command)), BotCommand):
                yield obj


class PrivateCommands(Commands):
    start = BotCommand(command="start", description="Start bot 💬")
    create_package = BotCommand(
        command="create_package", description="Create your own package 📦"
    )
    show_packages = BotCommand(
        command="show_packages", description="List of your packages 📬"
    )
    game_settings = BotCommand(
        command="game_settings", description="Configure the game ⚙️"
    )
    leave = BotCommand(command="leave", description="Leave from game 🚪")
    rules = BotCommand(command="rules", description="SpyGame rules 📖")
    help = BotCommand(
        command="help", description="See all commands and waht they do 🌚"
    )
    skip = BotCommand(command="skip", description="Skip action.")
    cancel = BotCommand(command="cancel", description="Cancel action.")


private = PrivateCommands()


class GroupCommands(Commands):
    play = BotCommand(command="play", description="Start the recruitment to game! 🎲")
    start_playing = BotCommand(
        command="start_playing", description="End recruitment and start play 🎮"
    )
    leave = private.leave
    vote = BotCommand(
        command="vote",
        description="Vote for spy! 🕵🏻‍♂️ Use @ after command to select user.",
    )
    join = BotCommand(command="join", description="Join to the game room. 👥")
    end = BotCommand(command="end", description="End the game. ⛔️")


group = GroupCommands()
