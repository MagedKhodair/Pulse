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

