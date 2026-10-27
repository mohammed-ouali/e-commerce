from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.sql import func

from sqlalchemy import (
    ForeignKey,
    Index,
    Integer,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.shared.model_mixins import TimestampMixin


class Wishlist(TimestampMixin, Base):
    __tablename__ = "wishlists"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    # ORM relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="wishlist",
    )

    items: Mapped[list["WishlistItem"]] = relationship(
        "WishlistItem",
        back_populates="wishlist",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class WishlistItem(Base):
    __tablename__ = "wishlist_items"

    __table_args__ = (
        Index("ix_wishlist_items_product_id", "product_id"),
        UniqueConstraint(
            "wishlist_id",
            "product_id",
            name="uq_wishlist_items_wishlist_product",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    wishlist_id: Mapped[int] = mapped_column(
        ForeignKey("wishlists.id", ondelete="CASCADE"),
        nullable=False,
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="RESTRICT"),
        nullable=False,
    )

    created_at: Mapped["datetime"] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # ORM relationships
    wishlist: Mapped["Wishlist"] = relationship(
        "Wishlist",
        back_populates="items",
    )

    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="wishlist_items",
    )
