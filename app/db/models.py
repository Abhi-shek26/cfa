from sqlalchemy import Column, Integer, String, Enum, Date # <-- Import Date
from .database import Base
import enum
from datetime import date # <-- Import date

# Define the SubscriptionTier enum to represent different subscription levels
class SubscriptionTier(str, enum.Enum):
    FREE = "free"
    PRO = "pro"
    PREMIUM = "premium"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    api_key = Column(String, unique=True, index=True, nullable=False)
    subscription_tier = Column(Enum(SubscriptionTier), default=SubscriptionTier.FREE, nullable=False)
    # Make requests_made non-nullable and default to 0
    requests_made = Column(Integer, default=0, nullable=False)
    # Add a new column to track the date
    last_request_date = Column(Date, default=date.today, nullable=False)
