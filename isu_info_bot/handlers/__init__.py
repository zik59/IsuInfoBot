from .cancel import register_handlers_cancel
from .group import register_handlers_group
from .help import register_handlers_help
from .process_any import register_handlers_process_any
from .start import register_handlers_start
from .student import register_handlers_student
from .variant import register_handlers_variant


__all__ = [
    "register_handlers_cancel",
    "register_handlers_group",
    "register_handlers_help",
    "register_handlers_process_any",
    "register_handlers_start",
    "register_handlers_student",
    "register_handlers_variant"
]
