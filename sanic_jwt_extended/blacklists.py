import abc

from datetime import datetime, timedelta


class Blacklist(abc.ABC):
    @abc.abstractmethod
    async def get_variable(self, name: str) -> str:
        pass

    @abc.abstractmethod
    async def set_variable(self, name: str, value: str):
        pass

    async def check_token(self, jwt_id: str):
        return (
            await self.get_variable(jwt_id) == "true"
            and datetime.fromisoformat(await self.get_variable(jwt_id + "_date"))
            > datetime.now()
        )

    async def blacklist_token(self, jwt_id: str, ban_for: timedelta):
        await self.set_variable(jwt_id, "true")
        await self.set_variable(
            jwt_id + "_date", (datetime.now() + ban_for).isoformat()
        )


class InMemoryBlacklist(Blacklist):
    def __init__(self):
        self.map = {}

    async def get_variable(self, name: str) -> str:
        return self.map.get(name, None)

    async def set_variable(self, name: str, value: str):
        self.map[name] = value
