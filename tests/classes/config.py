import os

class Config:
    @staticmethod
    def headless() -> bool:
        return os.environ.get("HEADLESS") == "true"

    @staticmethod
    def window_size() -> list:
        return os.environ.get("WINDOW_SIZE").split(",")
