from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal



# Request Schemas
class UserSignUp(BaseModel):
    user_id: str = Field(..., description="Unique user identifier")
    first_name: str = Field(..., min_length=1, max_length=100, description="First name is required, max 100 characters")
    last_name: str = Field(..., min_length=1, max_length=100, description="Last name is required, max 100 characters")
    address: Optional[str] = Field(None, max_length=500, description="Address is optional, max 500 characters")
    login_email: EmailStr = Field(..., description="Valid email address is required")
    membership_status: str = Field(default="Inactive", description="Membership tier for the user")

class MembershipStatusUpdate(BaseModel):
    membership_status: Literal["Inactive", "Active"]


# Response Schemas
class UserResponse(BaseModel): 
    user_id: str = Field(..., description="Unique user identifier")
    first_name: str = Field(..., description="User's first name")
    last_name: str = Field(..., description="User's last name")
    address: Optional[str] = Field(None, description="User's address")
    login_email: str = Field(..., description="User's email address")
    membership_status: str = Field(..., description="User's membership status")


class TransactionResponse(BaseModel):
    transaction_id: str = Field(..., description="Unique transaction identifier")
    user_id: str = Field(..., description="Identifier of the user associated with the transaction")
    transaction_date: str = Field(..., description="Date of the transaction")
    transaction_amount: float = Field(..., description="Total amount of the transaction")
    transaction_savings_amount: float = Field(..., description="Amount saved in the transaction")
    transaction_savings_percentage: float = Field(..., description="Percentage of savings in the transaction")
    price_adjustment_days_left: int = Field(..., description="Days left for price adjustment eligibility")
    item_count: int = Field(..., description="Number of items in the transaction")
    status : str = Field(..., description="Status of the transaction")
    merchant_name: str = Field(..., description="Name of the merchant associated with the transaction")

class TransactionItemResponse(BaseModel):
    product_title: str = Field(..., description="Title of the product in the transaction")
    quantity: int = Field(..., description="Quantity purchased")
    purchase_price: float = Field(..., description="Recorded purchase price")
    lowest_price: float = Field(..., description="Lowest observed price")
    total_price_difference_amount: float = Field(..., description="Total difference compared to the lowest price")

class UpdatedMembershipResponse(BaseModel):
    user_id: str = Field(..., description="Unique user identifier")
    membership_status: str = Field(..., description="Updated membership status")