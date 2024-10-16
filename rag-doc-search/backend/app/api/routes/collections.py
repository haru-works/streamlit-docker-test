import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select,delete

from app.api.deps import CurrentUser, SessionDep
from app.models import Collection, CollectionPublic, CollectionsPublic, Message

router = APIRouter()

@router.get("/list", response_model=CollectionsPublic)
def read_collections(
    session: SessionDep, current_user: CurrentUser, division_cd: str
) -> Any:
    """
    Retrieve collections.
    """

    count_statement = select(func.count()).select_from(Collection)
    count = session.exec(count_statement).one()
    statement = select(Collection).where(Collection.division_cd == division_cd)
    collections = session.exec(statement).all()

    if not collections:
        raise HTTPException(status_code=404, detail="collections not found")

    return CollectionsPublic(data=collections, count=count)


@router.post("/", response_model=CollectionPublic)
def create_collection(
    *, session: SessionDep, current_user: CurrentUser, collection_in: Collection
) -> Any:
    """
    Create new collection.
    """

    collection = Collection.model_validate(collection_in)

    session.add(collection)
    session.commit()
    session.refresh(collection)

    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")

    return collection


@router.delete("/all")
def delete_collection(
    session: SessionDep, current_user: CurrentUser, division_cd: str
) -> Message:
    """
    Delete a collection.
    """

    statement_select = select(Collection).where(Collection.division_cd == division_cd)
    res = session.exec(statement_select)
    collections = res.all()

    if not collections:
        raise HTTPException(status_code=404, detail="collections not found")
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    statement_delete = delete(Collection).where(Collection.division_cd == division_cd)
    session.exec(statement_delete)
    session.commit()

    return Message(message="collections all deleted successfully")

@router.delete("/one")
def delete_collection(
    session: SessionDep, current_user: CurrentUser, division_cd: str,collection_id: str
) -> Message:
    """
    Delete a collection.
    """

    statement_select = select(Collection).where(Collection.division_cd == division_cd).where(Collection.collection_id == collection_id)
    res = session.exec(statement_select)
    collection = res.one()

    if not collection:
        raise HTTPException(status_code=404, detail="collection not found")
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    statement_delete = delete(Collection).where(Collection.division_cd == division_cd).where(Collection.collection_id == collection_id)
    session.exec(statement_delete)
    session.commit()

    return Message(message="collection deleted successfully")

