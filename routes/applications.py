from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from database import engine

router = APIRouter()

with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            position TEXT NOT NULL,
            status TEXT NOT NULL,
            location TEXT
        )
    """))

    conn.commit()


class Application(BaseModel):
    company: str
    position: str
    status: str = "saved"
    location: str | None = None


class ApplicationResponse(BaseModel):
    id: int
    company: str
    position: str
    status: str
    location: str | None = None


@router.get(
    "/applications",
    response_model=list[ApplicationResponse],
    tags=["Applications"],
    summary="Get all applications"
)
def get_applications(status: str | None = None):

    with engine.connect() as conn:

        if status:
            result = conn.execute(
                text("""
                    SELECT * FROM applications
                    WHERE status = :status
                """),
                {"status": status}
            )

        else:
            result = conn.execute(
                text("SELECT * FROM applications")
            )

        rows = result.fetchall()

    applications = []

    for row in rows:
        applications.append({
            "id": row.id,
            "company": row.company,
            "position": row.position,
            "status": row.status,
            "location": row.location
        })

    return applications


@router.get(
    "/applications/{application_id}",
    response_model=ApplicationResponse,
    tags=["Applications"],
    summary="Get application by ID"
)
def get_application(application_id: int):

    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT * FROM applications
                WHERE id = :application_id
            """),
            {"application_id": application_id}
        )

        row = result.fetchone()

    if not row:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    return {
        "id": row.id,
        "company": row.company,
        "position": row.position,
        "status": row.status,
        "location": row.location
    }


@router.put(
    "/applications/{application_id}",
    response_model=ApplicationResponse,
    tags=["Applications"],
    summary="Edit an application"
)
def update_application(application_id: int, application: Application):

    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT * FROM applications
                WHERE id = :application_id
            """),
            {"application_id": application_id}
        )

        existing_application = result.fetchone()

        if not existing_application:
            raise HTTPException(
                status_code=404,
                detail="Application not found"
            )

        conn.execute(
            text("""
                UPDATE applications
                SET company = :company,
                    position = :position,
                    status = :status,
                    location = :location
                WHERE id = :application_id
            """),
            {
                "company": application.company,
                "position": application.position,
                "status": application.status,
                "location": application.location,
                "application_id": application_id
            }
        )

        conn.commit()

    return {
        "id": application_id,
        "company": application.company,
        "position": application.position,
        "status": application.status,
        "location": application.location
    }


@router.delete(
    "/applications/{application_id}",
    response_model=ApplicationResponse,
    tags=["Applications"],
    summary="Delete an application"
)
def delete_application(application_id: int):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT * FROM applications
                WHERE id = :application_id
            """),
            {"application_id": application_id}
        )

        application = result.fetchone()

        if not application:
            raise HTTPException(
                status_code=404,
                detail="Application not found"
            )

        conn.execute(
            text("""
                DELETE FROM applications
                WHERE id = :application_id
            """),
            {"application_id": application_id}
        )

        conn.commit()

    return {
        "message": "Application deleted"
    }


@router.post(
    "/applications",
    response_model=ApplicationResponse,
    status_code=201,
    tags=["Applications"],
    summary="Create a new application",
    description="Create and store a new job application in SQLite"
)
def create_application(application: Application):

    with engine.connect() as conn:
        result = conn.execute(
            text("""
                INSERT INTO applications (company, position, status, location)
                VALUES (:company, :position, :status, :location)
            """),
            {
                "company": application.company,
                "position": application.position,
                "status": application.status,
                "location": application.location
            }
        )

        conn.commit()

        application_id = result.lastrowid

    return {
        "id": application_id,
        "company": application.company,
        "position": application.position,
        "status": application.status,
        "location": application.location
    }