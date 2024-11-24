from utils.translate import TranslateStr
from spy.commands import private, group


SOMETHING_WRONG = TranslateStr("Something goes wrong, try again.")


SOMETHING_WRONG_TRY_START = TranslateStr(
    "Something goes wrong, use /start command and try again."
)


START_MSG = TranslateStr(
    """
Hello, {user.full_name}! 🎉

Welcome to the game "Spyfall"! 🕵️‍♂️ This bot will be your game host, making it easy to organize and play with your friends anytime. Just add me to a chat, and let’s get started!

What you can do:

Play with default locations and roles
- Don’t want to spend time setting up? Use the ready-made set of locations and roles I’ve prepared just for you.
"""
    + f"""
Create your own game packs -> /{private.create_package.command}
- Got unique ideas for locations and roles? Create your own custom pack and play with your friends your way.

Customize the game to your liking -> /{private.game_settings.command}

- Choose a specific pack if you want to try something new.
- Pick individual locations or roles to create a unique atmosphere.
- Set the number of rounds and the duration of each round.
- If you have big group to play you can play with two spies! 🕵️‍♂️🕵️‍♂️
- If two spies in game they can know each other and play together in team or no 👀

Host games effortlessly
- I’ll handle the rules, announce turns, start and end rounds, and even assist with voting for the suspect.

How to start?
- Read the rules -> /{private.rules.command}
- Use the /{private.help.command} command to learn available commands.
- Add me to a group chat with your friends and start a game with the /{group.play.command} command.

Ready for an adventure? Let’s find the spy together! 😏
"""
)


ADD_ME_TO_GROUP = TranslateStr("Add me to the group 🕵️‍♂️")


SKIPED_ACTION = TranslateStr("Action was skipped.")


CANCELED_ACTION = TranslateStr("Action was canceled.")


YOU_CANNOT_SKIP_THAT_ACTION = TranslateStr("You cannot skip that action.")


YOU_CANNOT_CANCEL_THAT_ACTION = TranslateStr("You cannot cancel that action.")


NAME_FOR_PACKAGE = TranslateStr(
    f"""
Enter the name for the package or click /{private.cancel.command} to cancel the action. 📦
> Example: "My first package"
"""
)


CANCELED = TranslateStr("Canceled.")


PACKAGE_ALREADY_EXISTS = TranslateStr("Package with {name} name already exists.")


PACKAGE_CREATED = TranslateStr("Package created!")
