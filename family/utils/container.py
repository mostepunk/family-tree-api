from dependency_injector import containers, providers

from family.adapters.db import Database
from family.services.accounts import AccountService, AccountUOW
from family.settings import db_settings

# from src.adapters.clients.aiohttp_client import AiohttpClient
# from src.adapters.clients.grpc.blog_client import BlogClient
# from src.adapters.db.database import Database
# from src.service_layer.publication_service import PublicationService
# from src.service_layer.unit_of_work.publication_uow import PublicationUnitOfWork
# from src.settings import db_settings


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["family.api"],
    )

    # Singleton
    db = providers.Singleton(Database, db_settings=db_settings)

    # Factory
    account_uow = providers.Factory(
        AccountUOW,
        session_factory=db.provided.session,
    )

    account_service = providers.Factory(
        AccountService,
        uow=account_uow,
    )
