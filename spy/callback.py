import enum


class CallbackPrefix(enum.StrEnum):
    delete_msg = "delete_message"

    show_packages = "show_packages"
    show_package = "sp:"
    delete_package = "dp:"
    choose_game_package = "cgp:"

    add_location = "al:"
    show_locations = "sls:"
    show_location = "sl:"
    delete_location = "dl:"
    add_game_location = "agl:"

    show_roles = "srs:"
    add_role = "ar:"
    show_role = "sr:"
    delete_role = "dr:"
    choose_game_roles = "cgr:"
    choose_role = "cr:"

    game_settings = "game_settings"
    select_game_package = "sgp:"
    choose_game_locations = "cgl:"
    select_roles_for_location = "srfl:"
    select_location_for_roles = "slfr:"
    configure_spies = "cfs:"
    configure_rounds = "cfr:"
    round_settings = "rs:"
    configure_round_time = "crt:"
    increase_round_time = "irt:"
    decrease_round_time = "drt:"
    increase_rounds = "ir:"
    decrease_rounds = "dcr:"
    set_two_spies = "sts:"
    set_spies_know_each_other = "sseo:"

    vote_per = "vote_per"
    vote_againts = "vote_againts"
    vote = "vote:"

    continue_guess = "continue_guess"
    guess_location = "gl:"
