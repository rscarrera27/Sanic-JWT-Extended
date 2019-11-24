import warnings
from abc import ABC, abstractmethod


class BlacklistABC(ABC):
    @abstractmethod
    def register(self, token):
        pass

    @abstractmethod
    def is_blacklisted(self, token):
        pass


class InMemoryBlacklist(BlacklistABC):
    def __init__(self):
        self.blacklist = []
        warnings.warn(
            "Using in-memory blacklist is not recommended for production environment"
        )

    def register(self, token):
        self.blacklist.append(token.jti)

    def is_blacklisted(self, token):
        return token.jti in self.blacklist


class RedisBlacklist(BlacklistABC):  # TODO implement
    def register(self, token):
        pass

    def is_blacklisted(self, token):
        pass
