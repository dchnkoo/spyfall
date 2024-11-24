from utils.translate import TranslateStr
from spy.commands import private, group
from settings import spygame


SOMETHING_WRONG = TranslateStr("Something goes wrong, click to /start and try again.")


SOMETHING_WRONG_TRY_START = TranslateStr(
    "Something goes wrong, use /start command and try again."
)


ADDED_SUCCESSFULY_SOME = TranslateStr("{some} added successfully!")


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


CLICK_ON_PACKAGE = TranslateStr(
    """
    Click on the package to select it. 📦

    If you doesn't choose any package, the game will be started with the random package.
    """
)


YOU_NEED_TO_SELECT_PACKAGE_FOR_SELECTING_LOCATIONS = TranslateStr(
    """
    You need to select the package first to select the locations. 📦
    """
)


PACKAGE_CREATED = TranslateStr("Package created!")


INFO_PACKAGES = TranslateStr(
    """
    Number of packages: {} 📮
    """
)

INFO_PACKAGE = TranslateStr(
    """
Package name: {package.name} 📦

Number of locations: {} 📍
"""
)


SHOW_PACKAGES = TranslateStr("Show packages 📦")


YOU_DOESNT_HAVE_ANY = TranslateStr("You doesn't have any {some} yet.")


YOU_DOESNT_HAVE_ANY_PACKAGE = YOU_DOESNT_HAVE_ANY.format(some="packages")


PACKAGE_WAS_DELETED = TranslateStr("Package was deleted!")


CLOSE_SOME = TranslateStr("Close {some} ✖️")


CLOSE_LIST = CLOSE_SOME.format(some="list")


DELETE_SOME = TranslateStr("Delete {some} 🗑")


DELETE_PACKAGE = DELETE_SOME.format(some="package")


SELECT_GAME_PACKAGE = TranslateStr("Select the game package. 📦")


ADD_SOME = TranslateStr("Add {some}")


ADD_LOCATION = ADD_SOME.format(some="location 📍")


LOCATIONS = TranslateStr("Locations 📍")


BACK = TranslateStr("Back ↩️")


ENTER_NAME = TranslateStr(
    """
Enter the name for the {some} or click /cancel to cancel the action.
> Example: {}
"""
)


ENTER_LOCATION_NAME = ENTER_NAME.format('"Hospital"', some="location")


ENTER_LINK_ON_IMAGE_OR_SKIP = TranslateStr(
    """
Enter the link on the image for the location or click /skip to skip this action. 🖼
> Example: "https://example.com/image.jpg"
"""
)


FAILED_TO_ADD_EXISTS = TranslateStr(
    """
Failed to add {some}. This {some} already exists.
"""
)


FAILED_TO_ADD_LIMIT = TranslateStr(
    """
Failed to add {some}. You have reached the limit of {some}s.
"""
)


FAILED_TO_ADD_LOCATION_EXIST = FAILED_TO_ADD_EXISTS.format(some="location")


FAILED_TO_ADD_LOCATION_LIMIT = FAILED_TO_ADD_LIMIT.format(some="location")


LOCATION_ADDED_SECCESSFULLY = ADDED_SUCCESSFULY_SOME.format(some="Location")


YOU_NEED_ADD_LOCATIONS_FOR_PACKAGE_TO_CHOOSE = TranslateStr(
    """
    You need to add locations for the package to choose them. 📍
    """
)


SELECT_GAME_LOCATIONS = TranslateStr(
    """
Select locations for your game. 📍

If you doesn't choose any location, the game will be started with the random location.
"""
)


SELECT_LOCATION_FOR_ROLE = TranslateStr(
    """
    Select the location for the choose roles. 📍
    """
)


INFO_LOCATION = TranslateStr(
    """
Location: {location.name} 📍

Roles: {} 👤
"""
)


CHOOSE_GAME_LOCATIONS = TranslateStr("Choose locations for the game. 📍")


YOU_PROVIDED_NOT_VALID_IMAGE = TranslateStr(
    "You provided not valid image. Try another link."
)


DELETE_LOCATION = DELETE_SOME.format(some="location")


ENTER_LINK_ON_IMAGE_OR_SKIP = TranslateStr(
    """
Enter the link on the image for the location or click /skip to skip this action. 🖼
> Example: "https://example.com/image.jpg"
"""
)


YOU_DOES_NOT_HAVE_LOCATIONS = YOU_DOESNT_HAVE_ANY.format(some="locations")


ROLES = TranslateStr("Roles 👥")


ADD_ROLE = ADD_SOME.format(some="role 👤")


DESCRIPTION_VALIDATION_ERROR = TranslateStr(
    "Description need to be less than 300 symbols."
)


FAILED_TO_ADD_ROLE_LIMIT = FAILED_TO_ADD_LIMIT.format(some="role")


FAILED_TO_ADD_ROLE_EXISTS = FAILED_TO_ADD_EXISTS.format(some="role")


ROLE_ADDED = ADDED_SUCCESSFULY_SOME.format(some="role")


ENTER_ROLE_NAME = ENTER_NAME.format('"Doctor"', some="role")


ENTER_ROLE_DESCRIPTION = TranslateStr(
    f"""
    Enter the description for the role or /skip this action. 👤

    Maximum {spygame.role_description_limit} characters.

    > Example: "Heal people"
    """
)


YOU_DOESNT_HAVE_ANY_ROLES = YOU_DOESNT_HAVE_ANY.format(some="roles")


ROLES_INFO = TranslateStr(
    """
Location: {location.name} 📍

Number of roles: {} 👤
"""
)


DELETE_ROLE = DELETE_SOME.format(some="role")


ROLE_INFO = TranslateStr(
    """
Role: {role.name} 👤

Description: {role.description}
"""
)


CHOOSE_GAME_ROLES = TranslateStr("Choose roles for the game. 👤")


YOU_NEED_ADD_ROLES_FOR_LOCATION_TO_CHOOSE = TranslateStr(
    """
    You need to add roles for the location to choose them. 👤
    """
)


SELECT_GAME_ROLES = TranslateStr(
    """
Select roles for your game. 👤

If you doesn't choose any role, the game will be random choose roles.
"""
)


CLOSE_MENU = CLOSE_SOME.format(some="menu")


CONFIGURE_SPIES = TranslateStr("Configure spies 🕵️‍♂️")


CONFIGURE_ROUNDS = TranslateStr("Configure game rounds 🎯")


GAME_SETTINGS = TranslateStr("Game settings 🎲")


ROUNDS_MENU = TranslateStr(
    """
In that menu you can configure how much rounds you want to play per one game and round duration ⌛️.

Current settings:
    Rounds: {rounds} 🎲
    Round duration: {round_duration} minute(s) ⏳
"""
)


NUMBER_OF_ROUNDS = TranslateStr("Number of rounds 🧩")


ROUND_TIME = TranslateStr("Round time ⚙️")


CONFIGURE_ROUND_TIME = TranslateStr(
    """
Configure round time ⚙️

⚠️ Recommendations for round time to number of players:
    3–4 players — 6 minutes
    5–6 players — 7 minutes
    7–8 players — 8 minutes
    9–10 players — 9 minutes
    11–12 players — 10 minutes

Current time: {time} minute(s) ⏱
"""
)


TIME_ERROR = TranslateStr(
    f"""
You cannot set round duration less than {spygame.min_round_time} and more than {spygame.max_round_time} minute(s).
"""
)


TIME_EDITED = TranslateStr(
    """
Round duration edited successfully! ✅
"""
)


CONFIGURE_NUMBER_OF_ROUNDS = TranslateStr(
    """
Configure number of rounds ⚙️

Current number of rounds: {rounds} 🎲
"""
)


ROUNDS_ERROR = TranslateStr(
    f"""
You cannot set less than {spygame.min_rounds} and more than {spygame.max_rounds} round(s).
"""
)


ROUNDS_EDITED = TranslateStr(
    """
Number of rounds edited successfully! ✅
"""
)


SET_TWO_SPIES = TranslateStr(
    """
    Two spies in game
    """
)


SPIES_KNOW_EACH_OTHER = TranslateStr(
    """
    Spies know each other
    """
)


SPIES_CONFIGURE_EXPLAIN = TranslateStr(
    """
    Configure the spies for the game. 🕵️‍♂️

    If you choose the option "Two spies in game", the game will be started with two spies and if you have more than 8 players.

    If you choose the option "Spies know each other", the spies will know each other in that game in opposite situation bot will not send message to spies about them.
    """
)
