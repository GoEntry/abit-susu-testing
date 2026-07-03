import os

class Config:
    @staticmethod
    def headless() -> bool:
        return os.environ.get("HEADLESS") == "true"

    @staticmethod
    def window_size() -> list:
        return os.environ.get("WINDOW_SIZE").split(",")

    @staticmethod
    def wp_admin_login() -> str:
        return os.environ.get("WP_ADMIN_LOGIN")

    @staticmethod
    def wp_admin_password() -> str:
        return os.environ.get("WP_ADMIN_PASSWORD")
