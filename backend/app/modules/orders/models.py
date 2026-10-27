
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    text,
)
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.shared.model_mixins import TimestampMixin
from app.shared.enums import OrderStatus


class Order(TimestampMixin, Base):
    __tablename__ = "orders"

    __table_args__ = (
        CheckConstraint(
            "payment_method = 'cash_on_delivery'",
            name="ck_orders_payment_method",
        ),
        CheckConstraint(
            "subtotal >= 0 AND delivery_fee >= 0 AND total >= 0",
            name="ck_orders_amounts_nonnegative",
        ),
        CheckConstraint(
            "total = subtotal + delivery_fee",
            name="ck_orders_total",
        ),
        Index("ix_orders_user_created", "user_id", "created_at"),
        Index("ix_orders_status_created", "status", "created_at"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Delivery contact snapshot
    first_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    last_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    customer_phone: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    wilaya: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    delivery_desk: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        SQLAlchemyEnum(
            OrderStatus,
            name="order_status",
            native_enum=False,
            create_constraint=True
        ),
        server_default=text("'PENDING'"),
        nullable=False,
    )

    payment_method: Mapped[str] = mapped_column(
        String(30),
        default="cash_on_delivery",
        server_default=text("'cash_on_delivery'"),
        nullable=False,
    )

    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    delivery_fee: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=Decimal("0.00"),
        server_default=text("0"),
        nullable=False,
    )

    total: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ORM relationships
    user: Mapped["User | None"] = relationship(
        "User",
        back_populates="orders",
    )

    items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem",
        back_populates="order",
        passive_deletes="all",
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    __table_args__ = (
        Index("ix_order_items_order_id", "order_id"),
        Index("ix_order_items_product_variant_id", "product_variant_id"),
        CheckConstraint(
            "quantity > 0",
            name="ck_order_items_quantity_positive",
        ),
        CheckConstraint(
            "unit_price >= 0 AND line_total >= 0",
            name="ck_order_items_amounts_nonnegative",
        ),
        CheckConstraint(
            "line_total = quantity * unit_price",
            name="ck_order_items_line_total",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="RESTRICT"),
        nullable=False,
    )

    product_variant_id: Mapped[int | None] = mapped_column(
        ForeignKey("product_variants.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Historical snapshots
    product_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    variant_attributes: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
        server_default=text("'{}'::jsonb"),
        nullable=False,
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    line_total: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    # ORM relationships
    order: Mapped["Order"] = relationship(
        "Order",
        back_populates="items",
    )

    product_variant: Mapped["ProductVariant | None"] = relationship(
        "ProductVariant",
        back_populates="order_items",
    )
