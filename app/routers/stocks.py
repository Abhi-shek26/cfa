from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional
from app.services import analysis
from app.schemas import stock as stock_schema
from app.security import auth

router = APIRouter(
    prefix="/indicators",
    tags=["indicators"],
    dependencies=[Depends(auth.rate_limiter)] # Apply rate limiter to all routes here
)

# Endpoint to get technical indicator data for a specific stock symbol
@router.get("/{indicator}/{symbol}", response_model=stock_schema.IndicatorResponse)
def get_indicator_data(
    symbol: str,
    indicator: str,
    # This combines authentication and authorization for the requested indicator
    user: auth.models.User = Depends(auth.get_current_user),
    # Get allowed date range based on tier
    allowed_dates: tuple = Depends(auth.get_date_range_for_tier),
    # Optional parameters for indicators
    period: Optional[int] = Query(20, description="Time period for SMA/EMA/Bollinger."),
    fast: Optional[int] = Query(12, description="Fast period for MACD."),
    slow: Optional[int] = Query(26, description="Slow period for MACD."),
    signal: Optional[int] = Query(9, description="Signal period for MACD."),
    std_dev: Optional[float] = Query(2.0, description="Standard deviation for Bollinger Bands.")
):
    # Perform the authorization check manually inside the function.
    auth.check_tier_authorization(user, indicator)
    start_date, end_date = allowed_dates

    indicator_data = analysis.get_technical_indicator(
        symbol=symbol.upper(),
        indicator=indicator.lower(),
        start_date=start_date,
        end_date=end_date,
        period=period,
        fast=fast,
        slow=slow,
        signal=signal,
        std_dev=std_dev
    )

    if indicator_data is None:
        raise HTTPException(status_code=404, detail=f"Data not found for symbol {symbol.upper()}")

    return {
        "symbol": symbol.upper(),
        "indicator": indicator.lower(),
        "data": indicator_data
    }
