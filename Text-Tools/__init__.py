from aqt import mw

from .config_dialog import register_config_action
from .config_store import migrate_config_if_needed
from .hooks import register_hooks

# Expose static web assets under /_addons/<addon_package>/...
mw.addonManager.setWebExports(__name__, r"web/.*\.(js|css)")

migrate_config_if_needed()
register_config_action()
register_hooks()
