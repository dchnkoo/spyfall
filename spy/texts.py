from spy.commands import private, group
from settings import spygame


SOMETHING_WRONG = r"Щось пішло не так\."


SOMETHING_WRONG_TRY_START = (
    SOMETHING_WRONG + r" Використайте команду /start та спробуйте знову\."
)


FIX = "Виправити 🔧"


COMMAND_ONLY_FOR_ADMINS = r"Ця команда тільки для адміністраторів\."


YOU_NEED_TO_GO_TO_THE_BOT = (
    SOMETHING_WRONG + r" Натисність на кнопку нижче та спробуйте знову\."
)


ADDED_SUCCESSFULY_SOME = r"{some} додано успішно\!"


START_MSG = (
    """
Привіт, {user.escaped_full_name}\\! 🎉

Ласкаво просимо до гри *"Знахідка для шпигуна"* 🕵️‍♂️
Цей бот стане вашим ведучим, допомагаючи легко організувати гру та грати з друзями в будь\\-який час\\. Просто додай мене в чат, і почнемо\\!
"""
    + f"""
*\\#\\#\\# Що я вмію:*

**🔹 Грай з готовими локаціями та ролями**
\\- Не хочеш витрачати час на налаштування? Використовуй набір локацій та ролей, який я вже підготував для тебе\\.

**🔹 Створюй власні ігрові набори** \\- {private.create_package}
\\- Є ідеї для унікальних локацій чи ролей? Створи свій власний набір і грай за своїми правилами\\.

**🔹 Налаштовуй гру під себе** \\- {private.game_settings}
\\- Обери конкретний набір, якщо хочеш спробувати щось нове\\.
\\- Вибери окремі локації чи ролі, щоб створити унікальну атмосферу\\.
\\- Налаштуй кількість раундів та тривалість кожного\\.
\\- У великих компаніях грайте з двома шпигунами 🕵️‍♂️🕵️‍♂️\\.
\\- Два шпигуни можуть знати один одного і грати в команді або залишатися в невіданні 👀\\.

**🔹 Легко веди ігри**
\\- Я подбаю про правила, оголошу хід, початок і закінчення раундів та навіть допоможу з голосуванням підозрюваних\\.

*\\#\\#\\# Як почати?*
\\- Ознайомся з правилами \\- {private.rules}
\\- Використовуй команду {private.help} для перегляду доступних команд\\.
\\- Додай мене до групового чату з друзями та запускай гру командою {group.play}\\.

Готовий до пригод? Давайте разом знайдемо шпигуна 😏
"""
)


ADD_ME_TO_GROUP = "Додай мене до групи 🕵️‍♂️"


SKIPED_ACTION = r"Дія була пропущена\."


CANCELED_ACTION = r"Дія була скасована\."


CANCEL = "Скасувати"


YOU_CANNOT_SKIP_THAT_ACTION = r"Ви не можете пропустити цю дію\."


YOU_CANNOT_CANCEL_THAT_ACTION = r"Ви не можете скасувати цю дію\."


NAME_FOR_PACKAGE = f"""
Введіть ім'я дял пакету або натисніть {private.cancel} щоб скасувати дію\\. 📦
\\> Приклад: "Мій перший пакет"
"""


CANCELED = r"Скасовано\."


PACKAGE_ALREADY_EXISTS = r"Пакет з {name} ім'ям вже існує\."


CLICK_ON_PACKAGE = r"""
    Натисніть на пакет щоб обрати його\. 📦

    Якщо ви не виберете жодного пакету він буде обраний під час гри автоматично\.
    """


YOU_NEED_TO_SELECT_PACKAGE_FOR_SELECTING_LOCATIONS = r"""
    Вам потрібно спочатку обрати пакет для того щоб обрати локації\. 📦
    """


PACKAGE_CREATED = r"Пакет створенний\!"


INFO_PACKAGES = """
    Кількість пакетів: {} 📮
    """

INFO_PACKAGE = """
Ім'я пакету: {package.escaped_name} 📦

Кількість локації: {} 📍
"""


SHOW_PACKAGES = "Показати мої пакети 📦"


YOU_DOESNT_HAVE_ANY = r"У вас ще немає {some}\."


YOU_DOESNT_HAVE_ANY_PACKAGE = YOU_DOESNT_HAVE_ANY.format(some="пакетів")


PACKAGE_WAS_DELETED = r"Пакет був видалений\!"


CLOSE_SOME = "Закрити {some} ✖️"


CLOSE_LIST = CLOSE_SOME.format(some="список")


DELETE_SOME = "Видалити {some} 🗑"


DELETE_PACKAGE = DELETE_SOME.format(some="пакет")


SELECT_GAME_PACKAGE = "Обрати ігровий пакет 📦"


ADD_SOME = "Додати {some}"


ADD_LOCATION = ADD_SOME.format(some="локацію 📍")


LOCATIONS = "Локації 📍"


BACK = "Назад ↩️"


ENTER_NAME = r"""
Введіть ім'я для {some} або натисність /cancel щоб скасувати дію\.
\> Приклад: {}
"""


ENTER_LOCATION_NAME = ENTER_NAME.format('"Лікарня"', some="локації")


ENTER_LINK_ON_IMAGE_OR_SKIP = r"""
Введіть посилання на зображення для локації або натисніть /skip щоб пропустити цю дію\. 🖼
\> Приклад: "https://example\.com/image\.jpg"
"""


FAILED_TO_ADD = r"Помилка при додаванні\."


FAILED_TO_ADD_EXISTS = FAILED_TO_ADD + r" Ця {some} вже існує\."


FAILED_TO_ADD_LIMIT = FAILED_TO_ADD + r" Ви досягли ліміту {some}\."


FAILED_TO_ADD_LOCATION_EXIST = FAILED_TO_ADD_EXISTS.format(some="локація")


FAILED_TO_ADD_LOCATION_LIMIT = FAILED_TO_ADD_LIMIT.format(some="локацій")


LOCATION_ADDED_SECCESSFULLY = ADDED_SUCCESSFULY_SOME.format(some="Локацію")


YOU_NEED_ADD_LOCATIONS_FOR_PACKAGE_TO_CHOOSE = r"""
    Вам потрібно додати локацій до пакету щоб обрати їх\. 📍
    """


SELECT_GAME_LOCATIONS = r"""
Оберіть локації для гри\. 📍

Якщо ви не виберете жодної локації, їх буде обрано автоматично під час гри\.
"""


SELECT_LOCATION_FOR_ROLE = r"""
    Оберіть локації для того щоб обрати ролі\. 📍
    """


INFO_LOCATION = """
Локація: {location.escaped_name} 📍

Ролі: {} 👤
"""


CHOOSE_GAME_LOCATIONS = "Оберіть локації для гри 📍"


YOU_PROVIDED_NOT_VALID_IMAGE = r"Ви надали хибне посилання\. Спробуйте інше\."


DELETE_LOCATION = DELETE_SOME.format(some="локацію")


YOU_DOES_NOT_HAVE_LOCATIONS = YOU_DOESNT_HAVE_ANY.format(some="локацій")


YOU_DOES_NOT_HAVE_LOCATIONS_IN_THAT_PACKAGE = (
    YOU_DOES_NOT_HAVE_LOCATIONS + r" В пакеті {}\."
)


ROLES = "Ролі 👥"


ADD_ROLE = ADD_SOME.format(some="роль 👤")


DESCRIPTION_VALIDATION_ERROR = r"Опис повинен бути менше 300 символів\."


FAILED_TO_ADD_ROLE_LIMIT = FAILED_TO_ADD_LIMIT.format(some="ролей")


FAILED_TO_ADD_ROLE_EXISTS = FAILED_TO_ADD_EXISTS.format(some="роль")


ROLE_ADDED = ADDED_SUCCESSFULY_SOME.format(some="Роль")


ENTER_ROLE_NAME = ENTER_NAME.format('"Доктор"', some="ролі")


ENTER_ROLE_DESCRIPTION = f"""
Ведіть опис для ролі або введіть команду /skip щоб пропустити\\. 👤

Максимум {spygame.role_description_limit} символів\\.

\\> Приклад: "Лікує людей"
"""


YOU_DOESNT_HAVE_ANY_ROLES = YOU_DOESNT_HAVE_ANY.format(some="ролей")


ROLES_INFO = """
Локаця: {location.escaped_name} 📍

Кількість ролей: {} 👤
"""


DELETE_ROLE = DELETE_SOME.format(some="роль")


ROLE_INFO = """
Роль: {role.escaped_name} 👤

Опис: {role.escaped_description}
"""


CHOOSE_GAME_ROLES = "Виберіть ролі для гри 👤"


YOU_NEED_ADD_ROLES_FOR_LOCATION_TO_CHOOSE = r"""
    Вам потрібно додати ролі для локації щоб обрати їх\. 👤
    """


SELECT_GAME_ROLES = r"""
Оберіть ролі для вашої гри\. 👤

Оберіть ролі для гри, якщо ви не оберете жодної ролі її буде обрано автоматично\.
"""


CLOSE_MENU = CLOSE_SOME.format(some="меню")


CONFIGURE_SPIES = "Налаштуйте шпигунів 🕵️‍♂️"


CONFIGURE_ROUNDS = "Налаштуйте раунди 🎯"


GAME_SETTINGS = "Ігрові налаштування 🎲"


ROUNDS_MENU = r"""
Тут ви можете налаштувати кількість раундів та час оного раунду ⌛️\.

Поточні налаштування:
    Раунди: {rounds} 🎲
    Час раунду: {round_duration} хв ⏳
"""


NUMBER_OF_ROUNDS = "Кількість раундів 🧩"


ROUND_TIME = "Час раунду ⚙️"


CONFIGURE_ROUND_TIME = r"""
Налаштування часу раунду ⚙️

⚠️ Рекомендації по часу раунду до кількості гравців:
    4 гравця \- 6 хвилин
    5–6 гравців \- 7 хвилин
    7–8 гравців \- 8 хвилин
    9–10 гравців \- 9 хвилин
    11–12 гравців \- 10 хвилин

Поточний час: {time} хв ⏱
"""


TIME_ERROR = f"""
Ви не можете встановити час раунду менший за {spygame.min_round_time} та більший за {spygame.max_round_time} хв.
"""


TIME_EDITED = "Час раунду відредаговано успішно ✅"


CONFIGURE_NUMBER_OF_ROUNDS = """
Налаштуйте кількість раундів ⚙️

Поточна кількість раундів: {rounds} 🎲
"""


ROUNDS_ERROR = f"""
Ви не можете встановити кількість раундів менший за {spygame.min_rounds} та більшу за {spygame.max_rounds}.
"""


ROUNDS_EDITED = "Кількість раундів відредаговано успішно ✅"


SET_TWO_SPIES = "Два шпигуни в грі"


SPIES_KNOW_EACH_OTHER = "Шпигуни знають один одного"


SPIES_CONFIGURE_EXPLAIN = f"""
    Налаштуйте шпигунів для гри\\. 🕵️‍♂️

    Якщо ви оберете опцію "{SET_TWO_SPIES}", гра розпочнеться з двома шпигунами якщо у вас більше {spygame.two_spies_limits_on_players} гравців\\.

    Якщо ви оберете опцію "{SPIES_KNOW_EACH_OTHER}", якщо у вас в грі два шпигуна то вибравши цю опцію кожному шпигуну буде надіслано повідомлення від бота про те хто другий шпигун, в іншому випадку він не буде цього робити та шпигуни не зможуть працювати в команді\\.
    """


NOTIFY_USER_ABOUT_ROLE = """
Твоя роль: {role.escaped_name} 👤
Опис ролі: {role.escaped_description}
"""


NOTIFY_ABOUT_LOCATION = "Локація: {location.escaped_name} 📍"


YOU_ALREADY_IN_GAME = r"Ти вже в грі\."


ROLES_LESS_THAN_PLAYERS = (
    r"Ролей менше ніж гравців в {} локації. Неможливо розпочати гру\."
)


YOU_NEED_MIN_THE_PLAYERS_TO_PLAY_WITH_TWO_SPIES = f"Вам потрібно мінімум {spygame.two_spies_limits_on_players} гравців щоб грати з двома шпигунами\\."


GAME_ROOM_ALREADY_FULL = r"Ігрова кімната вже повна\."


THE_SECOND_SPY_IS = r"""
    Другий шпигун це \- {player.markdown_user_link} 🕵️‍♂️
    """


SELECTED_LOCATIONS_NEED_TO_BE_MORE_THAN_ROUNDS = r"""
Локації які ви обираєте повинні бути більше ніжні кількість раундів\!

Поточна кількість обраних локації: {} 📍
Раундів: {} 🎯
"""


LOCATIONS_NEED_TO_BE_MORE_THAN_ROUNDS = r"""
Локацій в пакеті не достатньо щоб почати гру\. Локацій повинно бути більше ніж раундів\.

Кількість раундів: {} 📍
Раундів: {} 🎯
"""


BEGIN_ROUND = r"Початок {} раунду\!"


TO_END_OF_ROUND_REMAINS = r"До кінця раунду залишилось {} хв {} сек\."


GAME_ENDED = r"""
    Гра була закінчення\. 🕵️‍♂️
    """


RECRUITMENT_MESSAGE = f"""
🎲 *Розпочинається гра\\!* 🎲
Зараз відбувається набір гравців\\. У вас є *{spygame.recruitment_time // 60} хв* щоб приєднатися\\!

🔹 Щоб вийти з гри використовуйте команду `/leave`\\.

📢 Запрошуйте друзів \\- більше гравців, більше веселощів\\!
⌛ *Час пливе\\.\\.\\. Гра розпочнеться за {spygame.recruitment_time // 60} хв\\!*
"""


GAME_STARTED = r"""
🔥 *Гра розпочалася\!* 🔥

🔍 *Як це працює:*
1\. Кожному гравцю призначено роль:
Один або двоє з вас — це *Шпигун*, який не знає локації\.
Решта гравців знають локацію та мають конкретні ролі\.

2\. *Завдання гравців:* Виявити Шпигуна, задаючи хитрі запитання\.
Запитання мають допомагати викрити Шпигуна, не розкриваючи занадто багато про локацію\.

3\. *Завдання Шпигуна:* З’ясувати локацію або уникнути підозри до кінця раунду\.

4\. У кінці раунду відбудеться *фаза голосування*, де кожен голосує, хто, на їхню думку, є Шпигуном\.

5\. *Дострокове голосування \(опціонально\):* У будь\-який момент гри, якщо гравець впевнений, хто Шпигун, він може ініціювати *дострокове голосування* за допомогою команди `/vote @username`\.

⌛ *Тривалість раунду:* {} хв\.
🎲 *Кількість раундів у грі:* {} раунд\(и\|ів\)\.

🎭 Нехай гра розпочнеться\! Хід поточного гравця буде оголошено автоматично\.
"""


JOIN_TO_THE_GAME = "Приєднатися до гри 🕵️‍♂️"


RECRUITMENT_WILL_END = r"Набір закінчиться за {} секунд\."


DISPLAY_PLAYERS = "*В грі:*\n\n{}\n\n*Усього гравців:* {}"


GREETINGS_MSG_IN_GROUP = f"""
**🤖 Привіт усім\\! Я Ведучий гри "Знахідка для шпигуна"\\! 🕵️‍♂️**

Дякую, що додали мене до вашої групи\\! Я тут, щоб оживити досвід гри "Знахідка для шпигуна" 🎉\\. Ось що вам потрібно знати:

---

🛠 **Про мене:**
\\- Я допомагаю вам грати у **"Знахідка для шпигуна"**, захопливу гру таємниць і дедукції\\.
\\- Я розподіляю ролі, призначаю секретні локації та відстежую хід гри\\.

\\~\\~\\-\\-\\~\\~

🔑 **Необхідні дозволи:**
Щоб працювати належним чином, мені потрібні **права адміністратора** в цій групі\\. Будь ласка, переконайтеся, що я маю наступні дозволи:
1️⃣ **Закріплювати повідомлення** \\(для оголошень про гру\\)\\.
2️⃣ **Видаляти повідомлення** \\(щоб прибирати зайвий безлад\\)\\.
3️⃣ **Запрошувати користувачів через посилання** \\(для управління грою\\)\\.

Без цих дозволів я можу не впоратися з грою як слід\\.

\\~\\~\\-\\-\\~\\~

🎮 **Як розпочати гру:**
\\- Використовуйте команду `{group.play}`, щоб ініціювати нову гру\\.
\\- Я подбаю про все: від призначення ролей до управління ігровим процесом\\.

🕹 Готові грати? Надіть мені права адміністратора та введіть команду `{group.play}`, щоб почати\\!

\\~\\~\\-\\-\\~\\~

Давайте розпочнемо гру та з’ясуємо, хто шпигун\\! 🕵️‍♀️
"""


THIS_ROOM_DOESNT_EXISTS = "Цієї кімнати вже не існує\\."


YOU_JOINED_TO_THE_GAME = "Ви приєдналися до [гри]({})"


ASK_QUESTION_MSG = (
    """
*🔄 Наступний хід у грі "Знахідка для шпигуна"\\!*
🔍 *{}*, твій хід\\!
Задай запитання *{}*\\.

🎙️ *Приклад запитання:*
_"Що ти тут робиш\\?"_ або _"Як виглядає це місце\\?"_
"""
    + f"\nПісля цього передай хід наступному гравцю за допомогою команди {group.next}"
)


RESULTS_PREV_ROUND = "Результати після {} раунду:\n"


WINNERS = "Переможці гри з макс\\. кількістью балів:\n"


NO_WINNERS = r"В грі немає переможців\."


ROUND_START_IN = r"Раунд {} розпочнеться за {} сек\."


ROOM_NOT_FOUND = r"Ігрова кімната не знайдена\."


NOT_ENOUGH_PLAYERS_TO_START = f"Недостатньо гравців щоб розпочати гру\\. Мінімум потрібно {spygame.min_players_in_room} гравці\\."


NOT_ENOUGH_TO_DISTRIBUTE = f"Недостатньо гравців для розподілення завдань\\. Повинно бути хочаб {spygame.min_players_in_room} гравці\\."


PLAYER_LEFT_GAME = "{} вийшов з гри ⚠️"


NO_SPIES_FOR_CONTINUE = r"Немає шпигунів для продовження гри\."


CREATOR_LEFT_THE_GAME = r"Творець кімнати вийшов з гри\. Неможливо продовжити\."


NOT_ENOUGH_PLAYERS_TO_CONTINUE = f"Недостатньо гравців для продовження гри\\. Повинно бути хочаб {spygame.min_players_in_room} гравці\\."


NOT_CORRECT_MENTION_FOR_VOTE = f"Некоректне згадування користувача для голосування за нього\\.\n\nВикористовуйте `{group.vote} @suspected_username`"

YOU_CAN_VOTE_ONLY_FOR_USER_WHICH_IN_GAME = (
    r"Ви не можете голосувати за гравців, які зараз не беруть участь у грі\."
)

YOU_CANNOT_VOTE_FOR_YOUR_SELF = "Ви не можете голосувати за себе"

EARLY_VOTE = (
    r"🗣 {} вважає, що {} є шпигуном 🕵️‍♂️\. Якщо ви згодні, голосуйте нижче 📥"
    + f"\n\nУ вас є {spygame.early_vote_time} секунд для голосування\\."
)

SUMMARY_VOTING_MSG = f"""
Отже, раунд завершено, і вам потрібно проголосувати за гравця, якого ви підозрюєте у шпигунстві\\. У вас є {spygame.summmary_vote_time // 60} хвилин для обговорення та голосування\\.

Після того як ви віддали свій голос, скасувати його буде неможливо\\! ⚠️
"""

VOTE_FOR_SPY = r"Голосуйте за шпигуна 🕵🏻‍♂️\!"

YOU_ARE_NOT_IN_GAME = r"Ви не берете участі у грі\."

SUCCESSFULY_EARLY_VOTING = r"Успішне дострокове голосування\! Гравці виграють цей раунд, і всі, хто проголосував за шпигуна, отримують по одному балу\. Крім того, {} отримує один бонусний бал, оскільки виявив шпигуна\!"

NOT_SUCCESSFULY_EARLY_VOTING = r"Неуспішне дострокове голосування, ви всі проголосували за не шпигуна\. Кожен шпигун, який залишився в грі, отримає два бали\."

CONTINUE_THE_ROUND = r"У грі залишився ще один шпигун, і у вас є час, щоб спробувати знайти його та отримати більше балів за цей раунд\."

YOU_ALREADY_VOTED = "Ви вже проголосували."

YOU_VOTED = "Ви проголосували ✅"

SUSPECTED_CANNOT_VOTE_FOR_SELF = "Підозрюваний гравець не може голосувати за себе 🕵️‍♂️"

REDEFINED_LOCATION_ROLES_MESSAGE = "*⚠️ Локацію та ролі було перевизначено, перевірте свої нові ролі та локації у [чаті]({}) зі мною*"

ANYONE_WASNT_KICKED = r"Ніхто не був виключений із гри\. Якщо підозрюваний у шпигунстві був шпигуном, автор голосування отримує 1 бал\."

ANY_PLAYER_WASNT_KICKED = (
    r"Жодного гравця не було виключено з гри, ніхто не отримує бали\."
)

SUCCESSFULLY_SUMMARY_VOTE = r"Ви всі мали рацію, {link} був шпигуном\! Усі гравці, які проголосували за {link}, отримають 1 бал\."

UNSUCCESSFULLY_SUMMARY_VOTE = (
    r"{} не був шпигуном\. Лише шпигуни отримають по два бали кожен у цьому раунді\."
)

YOU_CAN_USE_THAT_COMMAND_ONLY_IF_YOU_SPY = (
    r"Ви можете використовувати цю команду лише якщо ви шпигун\."
)

WANRING_GUESS_MESSAGE = f"""
*⚠️ ПОПЕРЕДЖЕННЯ*

Якщо ви продовжите, усі гравці дізнаються, що ви шпигун 🕵️‍♂️

Щоб продовжити, натисніть на кнопку нижче\\. У вас буде {spygame.guess_location_time // 60} хвилин, щоб вгадати локацію або скасувати й спробувати пізніше\\.
"""

CONTINUE = "Продовжити"

NOTIFY_USERS_ABOUT_SPY = r"""
{} був шпигуном\! І, можливо, він зрозумів, яка це була локація\. Тепер він спробує її вгадати\.

Якщо він вгадає, то отримає 2 бали, а гравці програють цей раунд\. Якщо ви граєте з двома шпигунами, і вони знають один одного, обидва отримають по два бали, якщо один із них вгадає локацію\. У протилежному випадку всі гравці отримають по одному балу, і ми перейдемо до наступного раунду\.
"""

TRY_TO_GUESS = r"Спробуйте вгадати, натисніть на локацію, яка, на вашу думку, використовується зараз у грі\. Якщо ви виберете правильну локацію, отримаєте два бали\. Інакше ви нічого не отримаєте і програєте цей раунд\."

YOU_SUCCESSFULLY_GUESS_LOCATION = r"*Ви вгадали локацію і отримали два бали 🎉\!*"

YOU_UNSUCCESSFULLY_GUESS_LOCATION = (
    r"Ви не вгадали локацію\. Шпигуни програють цей раунд\."
)

SUCCESSFULLY_GUESS_LOCATION = r"""
_{} вгадав локацію {}_ і отримує 2 бали\! Гравці програють цей раунд 👀

__Якщо ви використовуєте двох шпигунів, і вони знають один одного, другий шпигун також отримує 2 бали\.__
"""

UNSUCCESSFULLY_GUESS_LOCATION = r"{} не вгадав локацію\. Шпигуни програють цей раунд\! Кожен гравець, який не є шпигуном, отримає 1 бал\!"

NOT_GUESS_LOCATION_IN_TIME = r"{} не вгадав локацію вчасно, і шпигуни програють цей раунд\. Кожен гравець, який не є шпигуном, отримає один бал\!"

YOU_DOESNT_GUESS_LOCATION_IN_TIME = (
    r"Ви не вгадали локацію вчасно і програєте цей раунд\."
)

CANNOT_CONTINUE_GAME_BECAUSE_BOT_BLOCKED = r"Хтось із вас заблокував мене\. Неможливо продовжити гру, створіть нову гру з активними гравцями\."
