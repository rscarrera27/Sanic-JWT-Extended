import abc

from datetime import datetime, timedelta


class Blacklist(abc.ABC):
    @abc.abstractmethod
    async def get_variable(self, name: str) -> str:
        """
        Abstract method that gets some kind of variable with a given name.
        If variable with a given name does not exist, return None.
        MUST not throw any exceptions.
        :param name: name of the variable
        :return: value of the variable
        """
        pass

    @abc.abstractmethod
    async def set_variable(self, name: str, value: str):
        """
        Abstract method that sets some kind of variable with a given name a given value.
        MUST not throw any exceptions.
        :param name: name of the variable
        :param value: value of the variable
        """
        pass

    async def check_token(self, jwt_id: str) -> bool:
        """
        Checks if the token is not banned at the moment.
        MUST not throw any exceptions.
        :param jwt_id: Some kind of id that's
        unique to the token. For example jti (https://tools.ietf.org/html/rfc7519#section-4.1.7)
        """
        return (
            await self.get_variable(jwt_id) == "true"
            and datetime.fromisoformat(await self.get_variable(jwt_id + "_date"))
            > datetime.now()
        )

    async def blacklist_token(self, jwt_id: str, blacklist_for: timedelta):
        """
        Blacklists token for a given time
        :param jwt_id: Some kind of id that's
        unique to the token. For example jti (https://tools.ietf.org/html/rfc7519#section-4.1.7)
        :param blacklist_for: For how much time should this token be banned
        """
        await self.set_variable(jwt_id, "true")
        await self.set_variable(
            jwt_id + "_date", (datetime.now() + blacklist_for).isoformat()
        )


class InMemoryBlacklist(Blacklist):
    def __init__(self):
        self.map = {}

    async def get_variable(self, name: str) -> str:
        return self.map.get(name, None)

    async def set_variable(self, name: str, value: str):
        self.map[name] = value
