import enum


class CallbackPrefix(enum.StrEnum):
    delete_msg = "delete_message"

    show_packages = "show_packages"
    show_package = "sp:"
    delete_package = "dp:"

    add_location = "al:"
    show_locations = "sls:"
    show_location = "sl:"
    delete_location = "dl:"

    show_roles = "sr:"
    add_role = "ar:"
