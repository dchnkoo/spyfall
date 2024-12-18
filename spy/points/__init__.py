from spy.routers import dp

from .start import private_only_msg_without_state
from .package import private_only_msg_without_state
from .location import private_only_msg_without_state, private_only_msg
from .roles import private_only_msg_without_state, private_only_msg
from .game_settings import private_only_msg_without_state
from .leave import private_only_msg_without_state
from .guess import private_only_msg_without_state
from .play import group_only_msg_without_state, group_clear, group_without_state
from .join import group_without_state
from .skip import private_only_msg
from .cancel import private_only_msg
from .delete import dp


dp.include_routers(
    group_only_msg_without_state,
    group_without_state,
    private_only_msg_without_state,
    private_only_msg,
    group_clear,
)
