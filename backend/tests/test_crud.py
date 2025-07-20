import pytest
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database.models import UserRole

def test_create_user(db_session: Session):
    """
    Test creating a new user.
    """
    user_in = schemas.UserCreate(
        username="testuser",
        password="testpassword123",
        role=UserRole.EXPERT
    )
    db_user = crud.create_user(db_session, user=user_in)
    
    assert db_user is not None
    assert db_user.username == "testuser"
    assert db_user.role == UserRole.EXPERT
    assert db_user.id is not None
    
    # Verify it's in the database
    retrieved_user = db_session.query(crud.models.User).filter(crud.models.User.id == db_user.id).first()
    assert retrieved_user is not None
    assert retrieved_user.username == "testuser"

def test_get_user_by_username(db_session: Session):
    """
    Test retrieving a user by their username.
    """
    user_in = schemas.UserCreate(
        username="testuser2",
        password="testpassword123",
        role=UserRole.ADMIN
    )
    crud.create_user(db_session, user=user_in)
    
    retrieved_user = crud.get_user_by_username(db_session, username="testuser2")
    
    assert retrieved_user is not None
    assert retrieved_user.username == "testuser2"
    assert retrieved_user.role == UserRole.ADMIN

def test_get_user(db_session: Session):
    """
    Test retrieving a user by their ID.
    """
    user_in = schemas.UserCreate(
        username="testuser3",
        password="testpassword123",
        role=UserRole.EXPERT
    )
    db_user = crud.create_user(db_session, user=user_in)
    
    retrieved_user = crud.get_user(db_session, user_id=db_user.id)
    
    assert retrieved_user is not None
    assert retrieved_user.id == db_user.id
    assert retrieved_user.username == "testuser3"

def test_get_users(db_session: Session):
    """
    Test retrieving multiple users.
    """
    # Create a few users
    crud.create_user(db_session, user=schemas.UserCreate(username="userA", password="passwordA1", role=UserRole.EXPERT))
    crud.create_user(db_session, user=schemas.UserCreate(username="userB", password="passwordB1", role=UserRole.ADMIN))
    
    users = crud.get_users(db_session, skip=0, limit=10)
    
    assert len(users) == 2
    assert users[0].username == "userA"
    assert users[1].username == "userB"

def test_update_user(db_session: Session):
    """
    Test updating a user's role and password.
    """
    user_in = schemas.UserCreate(
        username="updateuser",
        password="oldpassword1",
        role=UserRole.EXPERT
    )
    db_user = crud.create_user(db_session, user=user_in)
    
    # Update role
    user_update_role = schemas.UserUpdate(role=UserRole.ADMIN)
    updated_user = crud.update_user(db_session, user_id=db_user.id, user_update=user_update_role)
    
    assert updated_user.role == UserRole.ADMIN
    
    # Update password
    user_update_password = schemas.UserUpdate(password="newpassword1")
    updated_user = crud.update_user(db_session, user_id=db_user.id, user_update=user_update_password)
    
    # Password hash should have changed
    assert updated_user.password_hash != db_user.password_hash

def test_delete_user(db_session: Session):
    """
    Test deleting a user.
    """
    user_in = schemas.UserCreate(
        username="deleteuser",
        password="password123",
        role=UserRole.EXPERT
    )
    db_user = crud.create_user(db_session, user=user_in)
    
    deleted_user = crud.delete_user(db_session, user_id=db_user.id)
    assert deleted_user is not None
    
    # Verify user is deleted
    retrieved_user = crud.get_user(db_session, user_id=db_user.id)
    assert retrieved_user is None
