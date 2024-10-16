import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select,delete

from app.api.deps import CurrentUser, SessionDep
from app.models import Document, DocumentPublic, DocumentsPublic, Message

router = APIRouter()


@router.get("/collection-list", response_model=DocumentsPublic)
def read_documents(
    session: SessionDep, current_user: CurrentUser,division_cd: str,collection_id: str
) -> Any:
    """
    Retrieve documents by division_cd and collection_id.
    """

    statement = select(Document).where(Document.division_cd == division_cd).where(Document.collection_id == collection_id)
    res = session.exec(statement)
    documents = res.all()

    if not documents:
        raise HTTPException(status_code=404, detail="documents not found")

    return DocumentsPublic(data=documents)


@router.get("/one", response_model=DocumentPublic)
def read_document(session: SessionDep,current_user: CurrentUser,document_id: str) -> Any:
    """
    Get document by and document_id.
    """

    document = session.get(Document, document_id)

    if not document:
        raise HTTPException(status_code=404, detail="document not found")

    return document


@router.post("/", response_model=DocumentPublic)
def create_document(
    *, session: SessionDep, current_user: CurrentUser, document_in: Document
) -> Any:
    """
    Create new document.
    """

    document = Document.model_validate(document_in)

    session.add(document)
    session.commit()
    session.refresh(document)

    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")

    return document


@router.delete("/all")
def delete_documents_all(
    session: SessionDep, current_user: CurrentUser, division_cd: str,collection_id: str
) -> Message:
    """
    Delete all documents.
    """

    statement_select = select(Document).where(Document.division_cd == division_cd).where(Document.collection_id == collection_id)
    res = session.exec(statement_select)
    documents = res.all()

    if not documents:
        raise HTTPException(status_code=404, detail="documents not found")
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    statement_delete = delete(Document).where(Document.division_cd == division_cd).where(Document.collection_id == collection_id)
    session.exec(statement_delete)
    session.commit()

    return Message(message="documents all deleted successfully")


@router.delete("/one")
def delete_document(
    session: SessionDep, current_user: CurrentUser, division_cd: str,collection_id: str,document_id: str
) -> Message:
    """
    Delete a document.
    """

    statement = select(Document).where(Document.division_cd == division_cd).where(Document.collection_id == collection_id).where(Document.document_id == document_id)
    res = session.exec(statement)
    document = res.one()

    if not document:
        raise HTTPException(status_code=404, detail="document not found")
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    statement_delete = delete(Document).where(Document.division_cd == division_cd).where(Document.collection_id == collection_id).where(Document.document_id == document_id)
    session.exec(statement_delete)
    session.commit()

    return Message(message="document deleted successfully")