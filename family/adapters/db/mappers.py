from loguru import logger as logging
from sqlalchemy.orm import mapper, relationship
from src.adapters.db.models import invoice, invoice_item, payment_url, terminal
from src.domain.models import Invoice, InvoiceItem, PaymentUrl, Terminal


def start_mappers():
    logging.debug("Start mapping")
    mapper(
        Invoice,
        invoice,
        properties={
            "items": relationship(
                InvoiceItem, back_populates="invoice", lazy="selectin"
            )
        },
    )
    mapper(
        InvoiceItem,
        invoice_item,
        properties={
            "invoice": relationship(Invoice, back_populates="items", lazy="selectin")
        },
    )
    mapper(PaymentUrl, payment_url)
    mapper(Terminal, terminal)
    logging.debug("Mapping done")
