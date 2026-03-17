from fastapi import APIRouter, Depends # pyright: ignore[reportMissingImports]
from sqlalchemy.orm import Session # pyright: ignore[reportMissingImports]
from fastapi import HTTPException # pyright: ignore[reportMissingImports]
from app import models, schemas
from app.database import get_db
from app.auth import hash_password, verify_password, create_access_token, get_current_user, generate_api_key, get_current_project

router = APIRouter()

@router.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_pwd = hash_password(user.password)

    new_user = models.User(
        email=user.email,
        password=hashed_pwd
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# @router.get("/users", response_model=list[schemas.UserResponse])
# def get_users(
#     db: Session = Depends(get_db),
#     current_user: int = Depends(get_current_user)
# ):
#     users = db.query(models.User).all()
#     return users

@router.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@router.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(
    user_id: int,
    user_data: schemas.UserUpdate,
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_data.email is not None:
        user.email = user_data.email

    if user_data.password is not None:
        user.password = user_data.password

    db.commit()
    db.refresh(user)

    return user

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"detail": "User deleted"}

@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(db_user.id)})

    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserResponse)
def get_me(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    user = db.query(models.User).filter(models.User.id == current_user).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@router.post("/projects", response_model=schemas.ProjectResponse)
def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    api_key = generate_api_key()

    new_project = models.Project(
        name=project.name,
        api_key=api_key,
        owner_id=current_user
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project

@router.get("/projects", response_model=list[schemas.ProjectResponse])
def get_projects(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    projects = db.query(models.Project).filter(
        models.Project.owner_id == current_user
    ).all()

    return projects

@router.post("/projects/{project_id}/rotate-key", response_model=schemas.ProjectResponse)
def rotate_project_key(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    project = db.query(models.Project).filter(
        models.Project.id == project_id,
        models.Project.owner_id == current_user
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    project.api_key = generate_api_key()
    db.commit()
    db.refresh(project)

    return project

@router.get("/app/info")
def app_info(
    project = Depends(get_current_project)
):
    return {
        "project_id": project.id,
        "project_name": project.name,
        "owner_id": project.owner_id
    }