from fastapi import Security, HTTPException, Depends
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.db import models, database

api_key_header = APIKeyHeader(name="X-API-KEY")
rate_limit_store = {} # In-memory store for rate limiting

# This function retrieves the current user based on the provided API key.
def get_current_user(api_key: str = Security(api_key_header), db: Session = Depends(database.get_db)):
    """Authenticates a user based on API Key."""
    user = db.query(models.User).filter(models.User.api_key == api_key).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return user

# This function checks if the user's subscription tier allows access to a specific indicator.
def check_tier_authorization(user: models.User, indicator: str):
    """
    Checks if a user's subscription tier allows access to a given indicator.
    Raises HTTPException if not authorized.
    """
    tier = user.subscription_tier
    indicator_lower = indicator.lower()
    
    free_indicators = ['sma', 'ema']
    pro_indicators = free_indicators + ['rsi', 'macd']
    
    if tier == models.SubscriptionTier.PRO and indicator_lower not in pro_indicators:
        raise HTTPException(status_code=403, detail=f"Your Pro tier does not allow access to the '{indicator_lower}' indicator.")
    
    if tier == models.SubscriptionTier.FREE and indicator_lower not in free_indicators:
        raise HTTPException(status_code=403, detail=f"Your Free tier does not allow access to the '{indicator_lower}' indicator.")


# This function determines the date range for data access based on the user's subscription tier.
def get_date_range_for_tier(user: models.User = Depends(get_current_user)):
    """Determines the allowed data history based on subscription tier."""
    today = datetime.now()
    tier = user.subscription_tier
    
    if tier == models.SubscriptionTier.FREE:
        return (today - timedelta(days=90)).strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d')
    elif tier == models.SubscriptionTier.PRO:
        return (today - timedelta(days=365)).strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d')
    else: # Premium
        return '2020-01-01', today.strftime('%Y-%m-%d') # Assuming data starts from 2020

# This function implements a daily rate limiter based on the user's subscription tier.
def rate_limiter(user: models.User = Depends(get_current_user), db: Session = Depends(database.get_db)):
    """
    Implements tier-based daily rate limiting by checking and updating the database.
    """
    today = datetime.now().date()

    # If the last request was on a previous day, reset the counter
    if user.last_request_date < today:
        user.requests_made = 0
        user.last_request_date = today

    tier = user.subscription_tier
    
    limit = None
    if tier == models.SubscriptionTier.FREE:
        limit = 50
    elif tier == models.SubscriptionTier.PRO:
        limit = 500
        
    if limit is None: # Premium has no limit
        return

    # Check if the user's request count for today has exceeded the limit
    if user.requests_made >= limit:
        raise HTTPException(
            status_code=429, 
            detail="Daily rate limit exceeded. Please upgrade your plan or wait until tomorrow."
        )
    
    # Increment the user's request count and commit the change to the database
    user.requests_made += 1
    db.commit()
    db.refresh(user)