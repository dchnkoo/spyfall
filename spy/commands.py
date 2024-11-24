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
    rules = BotCommand(command="rules", description="SpyGame rules 📖")
    help = BotCommand(
        command="help", description="See all commands and waht they do 🌚"
    )
    skip = BotCommand(command="skip", description="Skip action.")
    cancel = BotCommand(command="cancel", description="Cancel action.")


class GroupCommands(Commands):
    play = BotCommand(command="play", description="Start the recruitment to game! 🎲")


private = PrivateCommands()
group = GroupCommands()
