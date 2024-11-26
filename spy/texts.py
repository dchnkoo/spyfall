from utils.translate import TranslateStr
from spy.commands import private, group
from settings import spygame


SOMETHING_WRONG = TranslateStr("Something goes wrong.")


SOMETHING_WRONG_TRY_START = TranslateStr(
    "Something goes wrong, use /start command and try again."
)


FIX = TranslateStr("Fix 🔧")


COMMAND_ONLY_FOR_ADMINS = TranslateStr("This command only for admins.")


YOU_NEED_TO_GO_TO_THE_BOT = TranslateStr(
    "Something goes wrong, click on button below and try again."
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


YOU_DOES_NOT_HAVE_LOCATIONS_IN_THAT_PACKAGE = YOU_DOES_NOT_HAVE_LOCATIONS.add(
    " In package {}."
)


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


NOTIFY_USER_ABOUT_ROLE = TranslateStr(
    """
Your role: {role.name} 👤
Role description: {role.description}
"""
)


NOTIFY_ABOUT_LOCATION = TranslateStr("Location: {location.name}")


YOU_ALREADY_IN_GAME = TranslateStr("You already in game.")


SELECTED_ROLES_LESS_THAN_PLAYERS = TranslateStr(
    "Selected roles less than players. Cannot start the game."
)


GAME_ROOM_ALREADY_FULL = TranslateStr("Game room already full.")


THE_SECOND_SPY_IS = TranslateStr(
    """
    The second spy is {player.markdown_user_link} 🕵️‍♂️
    """
)


SELECTED_LOCATIONS_NEED_TO_BE_MORE_THAN_ROUNDS = TranslateStr(
    """
Game locations which you selected need to be more than rounds!

Number of locations: {} 📍
Rounds: {} 🎯
"""
)


LOCATIONS_NEED_TO_BE_MORE_THAN_ROUNDS = TranslateStr(
    """
Locations in package not enough to start. Locations need to be more than rounds.

Number of locations: {} 📍
Rounds: {} 🎯
"""
)


BEGIN_ROUND = TranslateStr("Begin of {} round!")


TO_END_OF_ROUND_REMAINS = TranslateStr("The end of the round remains {} seconds")


GAME_ENDED = TranslateStr(
    """
    The game was ended. 🕵️‍♂️
    """
)


RECRUITMENT_MESSAGE = TranslateStr(
    r"""
🎲 *The game is starting\!* 🎲
We are now recruiting players to join the game\. You have *1 minute* to join\!

🔹 To join the game, click the button below or type `/join`\.
🔹 To leave the game, use `/leave`\.

📢 Invite your friends — the more players, the more fun\!
⌛ *The timer is ticking\.\.\. The game will begin in 1 minute\!*
"""
)


GAME_STARTED = TranslateStr(
    r"""
🔥 *The game has begun!* 🔥

🔍 *Here’s how it works:*
1. Each player has been assigned a role:
   - One or two of you is the *Spy*, who doesn’t know the location.
   - The rest of you know the location and have specific roles to play\.

2. *The players’ goal:* Identify the Spy by asking clever questions\.
   - Questions should help uncover the Spy without revealing too much about the location\.

3. *The Spy’s goal:* Figure out the location or avoid suspicion until the round ends\.

4. At the end of the round, there will be a *voting phase*, where everyone votes for who they believe the Spy is\.

5. *Optional Early Voting:* At any moment during the game, if a player is confident about who the Spy is, they can initiate *early voting* using the `/vote` command in [chat]({link}) with me\.

⌛ *Round duration:* {} minutes\.
🎲 *Game number of rounds:* {} rounds\.

🎭 Let the game begin\! The current player’s turn will be announced automatically\.
"""
)


JOIN_TO_THE_GAME = TranslateStr("Join to the game! 🕵️‍♂️")


RECRUITMENT_WILL_END = TranslateStr("Recruitment will end in {} seconds..")


DISPLAY_PLAYERS = TranslateStr("*In game:*\n\n{}\n\n*Total:* {}")


GREETINGS_MSG_IN_GROUP = TranslateStr(
    """
**🤖 Hello, everyone! I'm the Spyfall Game Master! 🕵️‍♂️**

Thank you for adding me to your group! I'm here to bring the Spyfall experience to life 🎉. Here's what you need to know:

---

🛠 **About Me:**
- I help you play **Spyfall**, a thrilling game of mystery and deduction.
- I'll manage roles, assign secret locations, and keep track of rounds.

~~---~~

🔑 **Permissions Required:**
To function properly, I need **Admin Rights** in this group. Please ensure I have the following permissions:
1️⃣ **Pin messages** (for game announcements).
2️⃣ **Delete messages** (to remove unnecessary clutter).
3️⃣ **Invite users via links** (to assist with game management).

Without these permissions, I might not be able to run the game smoothly.

~~---~~

🎮 **How to Start the Game:**
- Use the `/play` command to initiate a new game.
- I'll handle everything, from assigning roles to managing gameplay.

🕹 Ready to play? Grant me admin rights and type `/play` to begin!

~~---~~

Let's get the game rolling and find out who the spy is! 🕵️‍♀️
"""
)

THIS_ROOM_DOESNT_EXISTS = TranslateStr("That room doesn't exists already.")

YOU_JOINED_TO_THE_GAME = TranslateStr("You joined to the [game]({})")
