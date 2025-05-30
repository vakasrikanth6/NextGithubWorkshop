"""Data models for the VPP (Virtual Power Plant) application."""

from typing import Optional

from pydantic import BaseModel, Field


class Plant(BaseModel):
    """Represents a plant with capacity limits and current operational status."""

    id: int
    name: str
    max_capacity: float = Field(..., gt=0, description="Maximum power output in kW")
    min_capacity: float = Field(0, ge=0, description="Minimum power output in kW")
    status: Optional[str] = Field(
        "idle", description="Current status: idle/running/down"
    )


class DispatchRequest(BaseModel):
    """Request containing the total power demand to be dispatched."""

    demand: float = Field(..., gt=0, description="Total power demand to meet in kW")


class DispatchResponse(BaseModel):
    """Response containing dispatch allocations and unmet demand summary."""

    allocations: dict
    total_dispatched: float
    unmet_demand: float
