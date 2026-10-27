
from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Integer,
    SmallInteger,
    Text,
    Index,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.shared.model_mixins import TimestampMixin


class Review(TimestampMixin, Base):
    __tablename__ = "reviews"

    __table_args__ = (
        Index("ix_reviews_product_id", "product_id"),
        UniqueConstraint(
            "user_id",
            "product_id",
            name="uq_reviews_user_product",
        ),
        CheckConstraint(
            "rating BETWEEN 1 AND 5",
            name="ck_reviews_rating_range",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="RESTRICT"),
        nullable=False,
    )

    rating: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
    )

    comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ORM relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="reviews",
    )

    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="reviews",
    )
