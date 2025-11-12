from fastapi import APIRouter, HTTPException
import uuid
from datetime import datetime
from schemas import UserSignUp, UserResponse, UserSignIn
from db import execute_query, execute_command

# Change FastAPI to APIRouter
user_router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@user_router.post("/signup")
async def signup_user(user: UserSignUp):
    """Create a new user"""
    try:
        # Check if user already exists
        existing_users = await execute_query(
            "SELECT user_id FROM Application_User WHERE login_email = $1",
            user.login_email
        )
        
        if existing_users:  # If list is not empty
            raise HTTPException(status_code=400, detail="Email already registered")
        
        created_at = datetime.utcnow()
        
        # Insert new user using execute_command
        await execute_command("""
            INSERT INTO Application_User (user_id, first_name, last_name, address, login_email, created_at)
            VALUES ($1, $2, $3, $4, $5, $6)
        """, user.user_id, user.first_name, user.last_name, user.address, user.login_email, created_at)
        
        return UserResponse(
            user_id=user.user_id,
            first_name=user.first_name,
            last_name=user.last_name,
            address=user.address,
            login_email=user.login_email,
            created_at=str(created_at)
        )
    
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@user_router.post("/signin")
async def sign_in_user(credentials: UserSignIn):
    """Sign in a user by email"""
    try:
        # Find user using execute_query
        users = await execute_query("""
            SELECT user_id, first_name, last_name, address, login_email, created_at
            FROM Application_User
            WHERE login_email = $1
        """, credentials.login_email)
        
        if users:  # If list is not empty
            user = users[0]  # Get first (and should be only) result
            return UserResponse(
                user_id=str(user['user_id']),
                first_name=user['first_name'],
                last_name=user['last_name'],
                address=user['address'],
                login_email=user['login_email'],
                created_at=str(user['created_at'])
            )
        else:
            raise HTTPException(status_code=404, detail="User not found")
    
    except HTTPException:
        raise  # Re-raise HTTP exceptions  
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")