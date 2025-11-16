from typing import Optional
from fastapi import APIRouter, HTTPException
import uuid
from datetime import date, datetime
from schemas import TransactionResponse, UserSignUp, UserResponse, UserSignIn
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
    

purchase_router = APIRouter(
    prefix="/purchases",
    tags=["purchases"],
    responses={404: {"description": "Not found"}},
)

@purchase_router.get("/transactions/{user_id}", response_model=list[TransactionResponse])
async def fetch_transactions(user_id: str):
    rows = await execute_query("""
        SELECT
            transaction_id,
            user_id,
            transaction_date,
            transaction_amount,
            transaction_savings_amount,
            price_tracking_end_date,
            transaction_savings_percentage,
            item_count,
            merchant.merchant_name
        FROM app_schema.transaction
        JOIN app_schema.merchant ON transaction.merchant_id = merchant.merchant_id
        WHERE user_id = $1
    """, user_id)

    if not rows:
        raise HTTPException(status_code=404, detail="No transactions found for this user")

    today = date.today()

    def compute_days_left(end_date: datetime | None) -> int | None:
        if not end_date:
            return None
        end_day = end_date.date()
        if today >= end_day:
            return 0
        return (end_day - today).days
    
    def derive_status(days_left: Optional[int]) -> str:
        return "Inactive" if days_left == 0 or days_left is None else "Active"

    return [
        TransactionResponse(
            transaction_id=str(tx["transaction_id"]),
            user_id=str(tx["user_id"]),
            transaction_date=tx["transaction_date"].strftime("%d %B, %Y"),
            transaction_amount=float(tx["transaction_amount"]),
            transaction_savings_amount=float(tx["transaction_savings_amount"]),
            transaction_savings_percentage=float(tx["transaction_savings_percentage"]),
            price_adjustment_days_left=compute_days_left(tx["price_tracking_end_date"]),
            item_count=tx["item_count"],
            status=derive_status(compute_days_left(tx["price_tracking_end_date"])),
            merchant_name=tx["merchant_name"]

            
        )
        for tx in rows   # ← this loops through every row returned by the query
    ]