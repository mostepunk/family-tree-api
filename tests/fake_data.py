from tests.fake_const import admin


class FakeRepository:
    def __init__(self):
        self._fake_list = []
        self._fake_users = [admin]

    async def add(self, item):
        self._fake_list.append(item)

    async def get(self, reference):
        return next(b for b in self._fake_list if b.reference == reference)

    async def get_all(self):
        return self._fake_list

    async def get_list(self):
        return list(self._fake_list)

    async def get_or_create(self, *args):
        return self._fake_list

    async def get_by_username(self, username: str):
        # return next(b for b in self._fake_users if b.user_name == username)
        for user in self._fake_users:
            if user.user_name == username:
                return user


class FakeUOW:
    def __init__(self):
        self.committed = None
        self.accounts = FakeRepository()

    async def __aenter__(self):
        self.committed = False
        self.accounts = FakeRepository()

    async def __aexit__(self, *args):
        pass

    async def commit(self):
        self.committed = True

    async def rollback(self):
        pass
