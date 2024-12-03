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
Hello, {user.escaped_full_name}! 🎉

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

CANCEL = TranslateStr("Cancel")


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
Package name: {package.escaped_name} 📦

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


SELECT_GAME_PACKAGE = TranslateStr("Select the game package 📦")


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
Location: {location.escaped_name} 📍

Roles: {} 👤
"""
)


CHOOSE_GAME_LOCATIONS = TranslateStr("Choose locations for the game 📍")


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
Location: {location.escaped_name} 📍

Number of roles: {} 👤
"""
)


DELETE_ROLE = DELETE_SOME.format(some="role")


ROLE_INFO = TranslateStr(
    """
Role: {role.escaped_name} 👤

Description: {role.escaped_description}
"""
)


CHOOSE_GAME_ROLES = TranslateStr("Choose roles for the game 👤")


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
    4 players — 6 minutes
    5–6 players — 7 minutes
    7–8 players — 8 minutes
    9–10 players — 9 minutes
    11–12 players — 10 minutes

Current time: {time} minute(s) ⏱
"""
)


TIME_ERROR = TranslateStr(
    f"""
You cannot set round duration less than {spygame.min_round_time} and more than {spygame.max_round_time} minute(s)
"""
)


TIME_EDITED = TranslateStr(
    """
Round duration edited successfully ✅
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
You cannot set less than {spygame.min_rounds} and more than {spygame.max_rounds} round(s)
"""
)


ROUNDS_EDITED = TranslateStr(
    """
Number of rounds edited successfully ✅
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
Your role: {role.escaped_name} 👤
Role description: {role.escaped_description}
"""
)


NOTIFY_ABOUT_LOCATION = TranslateStr("Location: {location.escaped_name} 📍")


YOU_ALREADY_IN_GAME = TranslateStr("You already in game.")


ROLES_LESS_THAN_PLAYERS = TranslateStr(
    "Roles less than players in {} location. Cannot start the game."
)


YOU_NEED_MIN_THE_PLAYERS_TO_PLAY_WITH_TWO_SPIES = TranslateStr(
    f"You need minimum {spygame.two_spies_limits_on_players} players to play with two spies."
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


TO_END_OF_ROUND_REMAINS = TranslateStr(
    "To the end of the round remains in {} mintes {} seconds."
)


GAME_ENDED = TranslateStr(
    """
    The game was ended. 🕵️‍♂️
    """
)


RECRUITMENT_MESSAGE = TranslateStr(
    """
🎲 *The game is starting!* 🎲
We are now recruiting players to join the game. You have *1 minute* to join!

🔹 To join the game, click the button below or type `/join`.
🔹 To leave the game, use `/leave`.

📢 Invite your friends — the more players, the more fun!
⌛ *The timer is ticking... The game will begin in 1 minute!*
"""
)


GAME_STARTED = TranslateStr(
    """
🔥 *The game has begun!* 🔥

🔍 *Here’s how it works:*
1. Each player has been assigned a role:
One or two of you is the *Spy*, who doesn’t know the location.
The rest of you know the location and have specific roles to play.

2. *The players’ goal:* Identify the Spy by asking clever questions.
Questions should help uncover the Spy without revealing too much about the location.

3. *The Spy’s goal:* Figure out the location or avoid suspicion until the round ends.

4. At the end of the round, there will be a *voting phase*, where everyone votes for who they believe the Spy is.

5. *Optional Early Voting:* At any moment during the game, if a player is confident about who the Spy is, they can initiate *early voting* using the `/vote @username` command.

⌛ *Round duration:* {} minutes.
🎲 *Game number of rounds:* {} rounds.

🎭 Let the game begin! The current player’s turn will be announced automatically.
"""
)


JOIN_TO_THE_GAME = TranslateStr("Join to the game 🕵️‍♂️")


RECRUITMENT_WILL_END = TranslateStr("Recruitment will end in {} seconds")


DISPLAY_PLAYERS = TranslateStr("*In game:*\n\n{}\n\n*Total:* {}")


GREETINGS_MSG_IN_GROUP = TranslateStr(
    f"""
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
- Use the `/{group.play.command}` command to initiate a new game.
- I'll handle everything, from assigning roles to managing gameplay.

🕹 Ready to play? Grant me admin rights and type `/{group.play.command}` to begin!

~~---~~

Let's get the game rolling and find out who the spy is! 🕵️‍♀️
"""
)


THIS_ROOM_DOESNT_EXISTS = TranslateStr("That room doesn't exists already.")


YOU_JOINED_TO_THE_GAME = TranslateStr("You joined to the [game]({})")


ASK_QUESTION_MSG = TranslateStr(
    """
*🔄 Next turn in the "Spyfall" game!*
🔍 *{}*, it’s your turn!
Ask a question to *{}*.

🎙️ *Example question:*
_"What are you doing here?"_ or _"What does this place look like?"_
"""
    + f"\nAfter pass the turn to the next player /{group.next.command}"
)


RESULTS_PREV_ROUND = TranslateStr("Results after {} round:\n")


WINNERS = TranslateStr("Winners of game with max score:\n")


NO_WINNERS = TranslateStr("In game are'nt any winners.")


ROUND_START_IN = TranslateStr("Round {} will start in {} seconds.")


ROOM_NOT_FOUND = TranslateStr("Game room not found.")


NOT_ENOUGH_PLAYERS_TO_START = TranslateStr(
    f"Not enough players to start game. Minimum need {spygame.min_players_in_room} players."
)


NOT_ENOUGH_TO_DISTRIBUTE = TranslateStr(
    f"There are not enough players to distribute tasks. There must be at least {spygame.min_players_in_room} players."
)


PLAYER_LEFT_GAME = TranslateStr("{} left the game ⚠️")


NO_SPIES_FOR_CONTINUE = TranslateStr("No spies to continue the game.")


CREATOR_LEFT_THE_GAME = TranslateStr("Creator of room left the game. Cannot continue.")


NOT_ENOUGH_PLAYERS_TO_CONTINUE = TranslateStr(
    f"Not enough players to continue the game. There must be at least {spygame.min_players_in_room} players."
)


NOT_CORRECT_MENTION_FOR_VOTE = TranslateStr(
    f"Incorrect user mention for voting for him.\n\nUse `/{group.vote.command} @suspected_username`"
)


YOU_CAN_VOTE_ONLY_FOR_USER_WHICH_IN_GAME = TranslateStr(
    "You cannot vote for users which currently not in that game."
)


YOU_CANNOT_VOTE_FOR_YOUR_SELF = TranslateStr("You cannot vote for your self")


EARLY_VOTE = TranslateStr(
    "🗣 {} thinks the {} is spy 🕵️‍♂️. If you agree vote below 📥"
    + f"\n\nYou have {spygame.early_vote_time} seconds to vote."
)


SUMMARY_VOTING_MSG = TranslateStr(
    f"""
And so the round has come to an end and you need to vote for the player you think or suspect is a spy, you have {spygame.summmary_vote_time // 60} minutes to discuss among yourselves and vote.

Once you have cast your vote, it will no longer be possible to cancel it! ⚠️
"""
)


VOTE_FOR_SPY = TranslateStr("Vote for spy! 🕵🏻‍♂️")


YOU_ARE_NOT_IN_GAME = TranslateStr("You are not in game.")


SUCCESSFULY_EARLY_VOTING = TranslateStr(
    "Successfully early voting! Players win that round and every who voted per spy player get the one point, also {} get one bonus point beacause he's was detect the spy!"
)


NOT_SUCCESSFULY_EARLY_VOTING = TranslateStr(
    "Unsuccessfully early voting, you all voted for not spy player. Every spy player who still in game will receive two points."
)


CONTINUE_THE_ROUND = TranslateStr(
    "There is one more spy left in the game and you have time to try to find him and get more points for this round."
)


YOU_ALREADY_VOTED = TranslateStr("You already voted")


YOU_VOTED = TranslateStr("You voted ✅")


SUSPECTED_CANNOT_VOTE_FOR_SELF = TranslateStr(
    "Suspected player cannot vote for self 🕵️‍♂️"
)


REDEFINED_LOCATION_ROLES_MESSAGE = TranslateStr(
    "*⚠️ Just was redefine the location and roles, check your new roles and locations in [chat]({}) with me*"
)

ANYONE_WASNT_KICKED = TranslateStr(
    "Anyone wasn't excluded from game, if player which was suspected in spy was a spy, author of vote get the 1 point"
)


ANY_PLAYER_WASNT_KICKED = TranslateStr(
    "Any player wasnt kicked from game, any doesn't get the points."
)


SUCCESSFULLY_SUMMARY_VOTE = TranslateStr(
    "You all are right, {link} was a spy! All players which voted for the {link} will get 1 point."
)


UNSUCCESSFULLY_SUMMARY_VOTE = TranslateStr(
    "{} wasnt a spy, only spy players will get the 2 points each in that round."
)


YOU_CAN_USE_THAT_COMMAND_ONLY_IF_YOU_SPY = TranslateStr(
    "You can use that command only if you spy."
)


WANRING_GUESS_MESSAGE = TranslateStr(
    f"""
*⚠️ WARNING*

If you continue all players will know you're spy 🕵️‍♂️

To continue click on button below, you'll have {spygame.guess_location_time // 60} minutes to guess the location or cancel and try later.
"""
)


CONTINUE = TranslateStr("Continue")


NOTIFY_USERS_ABOUT_SPY = TranslateStr(
    """
{} was a spy! And maybe he understand what location it was, now he'll try to guess her.

If he guess he get 2 points and players will lose that round. If you play with two spies and they know each other, both will get two points if one of then guess the location, in oposite situation all players will get 1 point and we'll go to another round.
"""
)


TRY_TO_GUESS = TranslateStr(
    "Try to guess, click on location which you think used now in game, if you pick correct location you get two points in another way you get nothing and lose that round."
)


YOU_SUCCESSFULLY_GUESS_LOCATION = TranslateStr(
    "*You guessed location and get two points! 🎉*"
)


YOU_UNSUCCESSFULLY_GUESS_LOCATION = TranslateStr(
    "You're not guessed location. Spies lose that round."
)


SUCCESSFULLY_GUESS_LOCATION = TranslateStr(
    """
_{} guessed location {}_, he get 2 points! Players lose that round 👀

__If you use two spies and they know each other second spy too get 2 points.__
"""
)


UNSUCCESSFULLY_GUESS_LOCATION = TranslateStr(
    "{} doesn't guessed location. Spies lose that round! Every non-spy player will get 1 point!"
)


NOT_GUESS_LOCATION_IN_TIME = TranslateStr(
    "{} doesn't guessed location in time and spies lose that round, every non-spy player will get one point!"
)


YOU_DOESNT_GUESS_LOCATION_IN_TIME = TranslateStr(
    "You doesn't guessed location in time and lose that round."
)
