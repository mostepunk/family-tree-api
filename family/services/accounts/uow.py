from family.adapters.db.crud import AccountCRUD
from family.services.base.uow import BaseUOW


class AccountUOW(BaseUOW):
    async def __aenter__(self):
        self.session = self.session_factory()
        self.accounts = AccountCRUD(self.session)
