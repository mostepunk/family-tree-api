from sqlalchemy.ext.asyncio import AsyncSession


class BaseCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session
