from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Account(Base):
    __tablename__ = "account"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    external_auth_id: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    email: Mapped[str | None] = mapped_column(String(320), unique=True, index=True)
    display_name: Mapped[str | None] = mapped_column(String(64))
    password_hash: Mapped[str | None] = mapped_column(String(255))
    provider: Mapped[str] = mapped_column(String(32))
    status: Mapped[str] = mapped_column(String(32), default="ACTIVE", index=True)
    roles: Mapped[str] = mapped_column(Text, default="player")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    characters: Mapped[list["Character"]] = relationship(back_populates="account")


class Character(Base):
    __tablename__ = "character"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    account_id: Mapped[UUID] = mapped_column(ForeignKey("account.id"), index=True)
    name: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    gender: Mapped[str] = mapped_column(String(16), default="UNSET")
    level: Mapped[int] = mapped_column(default=1)
    xp: Mapped[int] = mapped_column(default=0)
    status: Mapped[str] = mapped_column(String(32), default="ACTIVE", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    account: Mapped[Account] = relationship(back_populates="characters")
    inventory_items: Mapped[list["InventoryItem"]] = relationship(back_populates="character")
    quests: Mapped[list["CharacterQuest"]] = relationship(back_populates="character")


class InventoryItem(Base):
    __tablename__ = "inventory_item"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    character_id: Mapped[UUID] = mapped_column(ForeignKey("character.id"), index=True)
    item_template_code: Mapped[str] = mapped_column(String(128))
    quantity: Mapped[int] = mapped_column(default=1)
    status: Mapped[str] = mapped_column(String(32), default="ACTIVE")

    character: Mapped[Character] = relationship(back_populates="inventory_items")


class Quest(Base):
    __tablename__ = "quest"

    code: Mapped[str] = mapped_column(String(64), primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    summary: Mapped[str] = mapped_column(String(512))
    objective: Mapped[str] = mapped_column(String(256))
    required_progress: Mapped[int] = mapped_column(default=1)
    reward_xp: Mapped[int] = mapped_column(default=0)
    sort_order: Mapped[int] = mapped_column(default=0)
    status: Mapped[str] = mapped_column(String(32), default="ACTIVE", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class CharacterQuest(Base):
    __tablename__ = "character_quest"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    character_id: Mapped[UUID] = mapped_column(ForeignKey("character.id"), index=True)
    quest_code: Mapped[str] = mapped_column(ForeignKey("quest.code"))
    state: Mapped[str] = mapped_column(String(32), default="IN_PROGRESS")
    progress: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    character: Mapped[Character] = relationship(back_populates="quests")
    quest: Mapped[Quest] = relationship()
