from .start import private_only_msg_without_state
from .package import private_only_msg_without_state
from .skip import private_only_msg
from .cancel import private_only_msg


from spy.routers import dp

dp.include_routers(
    private_only_msg_without_state,
    private_only_msg,
)
