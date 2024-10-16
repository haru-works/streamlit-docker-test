import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import Division, DivisionPublic, DivisionsPublic, Message

router = APIRouter()

@router.get("/list", response_model=DivisionsPublic)
def read_divisions(
    session: SessionDep, current_user: CurrentUser,
) -> Any:
    """
    Retrieve divisions.
    """
    count_statement = select(func.count()).select_from(Division)
    count = session.exec(count_statement).one()
    statement = select(Division)
    divisions = session.exec(statement).all()

    if not divisions:
        raise HTTPException(status_code=404, detail="divisions not found")

    return DivisionsPublic(data=divisions, count=count)


@router.get("/one", response_model=DivisionPublic)
def read_division(session: SessionDep, current_user: CurrentUser, division_cd: str) -> Any:
    """
    Get division by division_cd.
    """
    division = session.get(Division, division_cd)

    if not division:
        raise HTTPException(status_code=404, detail="division not found")

    return division

@router.post("/", response_model=DivisionPublic)
def create_division(
    *, session: SessionDep, current_user: CurrentUser, division_in: Division
) -> Any:
    """
    Create new division.
    """

    division = Division.model_validate(division_in)

    session.add(division)
    session.commit()
    session.refresh(division)

    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")

    return division

@router.put("/", response_model=DivisionPublic)
def update_item(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    division_cd: str,
    division_in: Division
) -> Any:
    """
    Update an division.
    """

    division = session.get(Division, division_cd)

    if not division:
        raise HTTPException(status_code=404, detail="division not found")
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    update_dict = division_in.model_dump(exclude_unset=True)
    division.sqlmodel_update(update_dict)
    session.add(division)
    session.commit()
    session.refresh(division)

    return division


@router.delete("/")
def delete_division(
    session: SessionDep, current_user: CurrentUser, division_cd: str
) -> Message:
    """
    Delete a division.
    """

    division = session.get(Division, division_cd)

    if not division:
        raise HTTPException(status_code=404, detail="division not found")
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    session.delete(division)
    session.commit()

    return Message(message="division deleted successfully")