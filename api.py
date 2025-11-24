from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request
from datetime import date, datetime
from auth import get_current_user
from schemas import MembershipStatusUpdate, TransactionResponse, UserSignUp, UserResponse, TransactionItemResponse, UpdatedMembershipResponse
from db import execute_query, execute_command

# Change FastAPI to APIRouter
user_router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@user_router.post("/create_profile")
async def create_profile(user: UserSignUp, current_user: dict = Depends(get_current_user)):
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
            INSERT INTO Application_User (user_id, first_name, last_name, address, login_email, membership_status)
            VALUES ($1, $2, $3, $4, $5, $6)
        """, user.user_id, user.first_name, user.last_name, user.address, user.login_email, user.membership_status)
        
        return UserResponse(
            user_id=user.user_id,
            first_name=user.first_name,
            last_name=user.last_name,
            address=user.address,
            login_email=user.login_email,
            membership_status=user.membership_status
        )
    
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@user_router.get("/get_profile")
async def get_profile(current_user: dict = Depends(get_current_user)):
    """Get the profile of the current user"""
    try:
        # Find user using execute_query
        users = await execute_query("""
            SELECT user_id, first_name, last_name, address, login_email, membership_status
            FROM Application_User
            WHERE user_id = $1
        """, current_user["uid"])
        
        if users:  # If list is not empty
            user = users[0]  # Get first (and should be only) result
            return UserResponse(
                user_id=str(user['user_id']),
                first_name=user['first_name'],
                last_name=user['last_name'],
                address=user['address'],
                login_email=user['login_email'],
                membership_status=user['membership_status']
            )
        else:
            raise HTTPException(status_code=404, detail="User not found")
    
    except HTTPException:
        raise  # Re-raise HTTP exceptions  
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
@user_router.patch("/membership_status_update")
async def update_membership_status(Payload: MembershipStatusUpdate, current_user: dict = Depends(get_current_user)):
    """Update the membership status of the current user"""
    try:
        new_status = Payload.membership_status
        user_id = current_user["uid"]
        
        # Update membership status using execute_command
        result = await execute_command("""
            UPDATE Application_User
            SET membership_status = $1
            WHERE user_id = $2
        """, new_status, user_id)
        
        if result == 0: # Post update guard
            raise HTTPException(status_code=404, detail="User not found")
        
        return UpdatedMembershipResponse(
            user_id=user_id,
            membership_status=new_status
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

purchase_router = APIRouter(
    prefix="/purchases",
    tags=["purchases"],
    responses={404: {"description": "Not found"}},
)

@purchase_router.get("/transaction/{transaction_id}", response_model=TransactionResponse)    
async def fetch_transaction(transaction_id: str, current_user: dict = Depends(get_current_user)):
    user_id = current_user["uid"]
    result = await execute_query(
        """
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
        WHERE user_id = $1 AND transaction_id = $2
        """,
        user_id,
        transaction_id
    )

    if not result:
        raise HTTPException(status_code=404, detail="No transactions found for this user")

    row = result[0]  # Get the first (and only) row from the result
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

    return TransactionResponse(
            transaction_id=str(row["transaction_id"]),
            user_id=str(row["user_id"]),
            transaction_date=row["transaction_date"].strftime("%d %B, %Y"),
            transaction_amount=float(row["transaction_amount"]),
            transaction_savings_amount=float(row["transaction_savings_amount"]),
            transaction_savings_percentage=float(row["transaction_savings_percentage"]),
            price_adjustment_days_left=compute_days_left(row["price_tracking_end_date"]),
            item_count=row["item_count"],
            status=derive_status(compute_days_left(row["price_tracking_end_date"])),
            merchant_name=row["merchant_name"]
        )


@purchase_router.get("/transactions", response_model=list[TransactionResponse])
async def fetch_transactions(current_user: dict = Depends(get_current_user)):
    user_id = current_user["uid"]

    current_user: dict = Depends(get_current_user)
    rows = await execute_query(
        """
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
        """,
        user_id,
    )

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
            transaction_id=str(["transaction_id"]),
            user_id=str(["user_id"]),
            transaction_date=["transaction_date"].strftime("%d %B, %Y"),
            transaction_amount=float(["transaction_amount"]),
            transaction_savings_amount=float(["transaction_savings_amount"]),
            transaction_savings_percentage=float(["transaction_savings_percentage"]),
            price_adjustment_days_left=compute_days_left(["price_tracking_end_date"]),
            item_count=["item_count"],
            status=derive_status(compute_days_left(["price_tracking_end_date"])),
            merchant_name=["merchant_name"],
        )
        for row in rows
    ]




@purchase_router.get("/items/{transaction_id}", response_model=list[TransactionItemResponse])
async def fetch_transaction_items(transaction_id: str, current_user: dict = Depends(get_current_user)):
    user_id = current_user["uid"]
    rows = await execute_query(
        """
        SELECT
            product.title AS product_title,
            item.quantity,
            item.purchase_price,
            item.lowest_price,
            item.total_price_difference_amount
        FROM app_schema.item
        JOIN app_schema.product
            ON item.product_id = product.product_id
        JOIN app_schema.transaction
            ON item.transaction_id = transaction.transaction_id
        WHERE transaction.user_id = $1
          AND item.transaction_id = $2
        """,
        user_id,
        transaction_id,
    )
    if not rows:
        raise HTTPException(status_code=404, detail="No items found for this transaction")

    return [
        TransactionItemResponse(
            product_title=row["product_title"],
            quantity=row["quantity"],
            purchase_price=float(row["purchase_price"]),
            lowest_price=float(row["lowest_price"]),
            total_price_difference_amount=float(row["total_price_difference_amount"]),
        )
        for row in rows
    ]

