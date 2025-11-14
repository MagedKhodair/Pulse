from pydantic import BaseModel, EmailStr, Field
from typing import Optional



# Request Schemas
class UserSignUp(BaseModel):
    user_id: str = Field(..., description="Unique user identifier")
    first_name: str = Field(..., min_length=1, max_length=100, description="First name is required, max 100 characters")
    last_name: str = Field(..., min_length=1, max_length=100, description="Last name is required, max 100 characters")
    address: Optional[str] = Field(None, max_length=500, description="Address is optional, max 500 characters")
    login_email: EmailStr = Field(..., description="Valid email address is required")

class UserSignIn(BaseModel):
    login_email: EmailStr = Field(..., description="Email address for authentication")


# Response Schemas
class UserResponse(BaseModel): 
    user_id: str = Field(..., description="Unique user identifier")
    first_name: str = Field(..., description="User's first name")
    last_name: str = Field(..., description="User's last name")
    address: Optional[str] = Field(None, description="User's address")
    login_email: str = Field(..., description="User's email address")
    created_at: str = Field(..., description="Account creation timestamp")


class TransactionResponse(BaseModel):
    transaction_id: str = Field(..., description="Unique transaction identifier")
    user_id: str = Field(..., description="Identifier of the user associated with the transaction")
    merchant_id: str = Field(..., description="Identifier of the merchant involved in the transaction")
    transaction_date: str = Field(..., description="Date of the transaction")
    transaction_amount: float = Field(..., description="Total amount of the transaction")
    transaction_savings_amount: float = Field(..., description="Amount saved in the transaction")
    price_tracking_end_date: str = Field(..., description="End date for price tracking")
    transaction_savings_percentage: float = Field(..., description="Percentage of savings in the transaction")
    created_at: str = Field(..., description="Timestamp when the transaction was created")
    price_adjustment_days_left: int = Field(..., description="Days left for price adjustment eligibility")