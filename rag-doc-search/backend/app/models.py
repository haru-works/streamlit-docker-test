import uuid

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional
from datetime import datetime


# User ベースプロパティ
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)
    division_cd: str = Field(default=None, max_length=255)


# User 作成時のプロパティ
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)

# User 登録のプロパティ
class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


# User 更新時のプロパティ
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)

# User 更新時のプロパティ
class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)

# User パスワード更新のプロパティ
class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# Userテーブル
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)


# API経由で返す型
class UserPublic(UserBase):
    id: uuid.UUID


# API経由で返すリスト型
class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int



# Item ベースプロパティ
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Item 作成時のプロパティ
class ItemCreate(ItemBase):
    pass


# Item 更新時のプロパティ
class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# Item テーブル
class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="items")


# API経由で返す型
class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID

# API経由で返すリスト型
class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None

# 新パスワードプロパティ
class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)


# Division テーブル
class Division(SQLModel, table=True):
    division_cd: str = Field(default=None, max_length=255,primary_key=True)
    division_name: str = Field(default=None, max_length=255)
    create_user: str = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    update_user: str = Field(default=None, max_length=255)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)
    delete_flg: bool = Field(default=False, nullable=False)

# Select用
class DivisionBase(SQLModel):
    division_name: str
    create_user: str
    created_at: datetime
    update_user: str
    updated_at: datetime
    delete_flg: bool 

# API経由で返す型
class DivisionPublic(DivisionBase):
    division_cd: str

# API経由で返すリスト型
class DivisionsPublic(SQLModel):
    data: list[DivisionPublic]
    count: int


# Collection テーブル
class Collection(SQLModel, table=True):
    collection_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    collection_name: str = Field(default=None, max_length=2000)
    division_cd: str = Field(default=None, max_length=255)
    create_user: str = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    update_user: str = Field(default=None, max_length=255)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)

# Select用
class CollectionBase(SQLModel):
    collection_name: str 
    division_cd: str 
    create_user: str
    created_at: datetime 
    update_user: str 
    updated_at: datetime 

# API経由で返す型
class CollectionPublic(CollectionBase):
    collection_id: uuid.UUID 

# API経由で返すリスト型
class CollectionsPublic(SQLModel):
    data: list[CollectionPublic]
    count: int


# Document テーブル
class Document(SQLModel, table=True):
    document_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    document_name: str = Field(default=None, max_length=4000)
    document_full_path: str = Field(default=None, max_length=4000)
    collection_id: uuid.UUID = Field(default=None)
    collection_name: str = Field(default=None, max_length=2000)
    division_cd: str = Field(default=None, max_length=255)
    create_user: str = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    update_user: str = Field(default=None, max_length=255)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)

# Select用
class DocumentBase(SQLModel):
    document_name: str 
    document_full_path: str 
    collection_id: uuid.UUID 
    collection_name: str 
    division_cd: str 
    create_user: str 
    created_at: datetime 
    update_user: str 
    updated_at: datetime 


# API経由で返す型
class DocumentPublic(DocumentBase):
    document_id: uuid.UUID

# API経由で返すリスト型
class DocumentsPublic(SQLModel):
    data: list[Document]
