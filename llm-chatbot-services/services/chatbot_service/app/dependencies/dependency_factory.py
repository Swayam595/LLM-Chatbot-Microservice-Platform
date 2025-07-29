from config import AppConfig

_app_config = AppConfig()

def get_app_config() -> AppConfig:
    """Get the app config"""
    return _app_config