"""FastAPI app for managing a Virtual Power Plant (VPP).

This API supports plant registration, querying plant data,
aggregating available power, and dispatching power based on demand.
"""

from typing import Dict

from fastapi import FastAPI, HTTPException

from .models import DispatchRequest, DispatchResponse, Plant

app = FastAPI(title="Virtual Power Plant API")

plants: Dict[int, Plant] = {}
next_id = 1


@app.post("/plants/", response_model=Plant)
def register_plant(plant: Plant):
    """Register a new plant and assign it a unique ID."""
    global next_id
    plant.id = next_id
    plants[next_id] = plant
    next_id += 1
    return plant


@app.get("/plants/", response_model=list[Plant])
def list_plants():
    """Return a list of all registered plants."""
    return list(plants.values())


@app.get("/plants/{plant_id}", response_model=Plant)
def get_plant(plant_id: int):
    """Retrieve details of a specific plant by its ID."""
    plant = plants.get(plant_id)
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    return plant


@app.get("/aggregate/")
def aggregate_power():
    """Calculate and return the total available power from active plants."""
    total = sum(p.max_capacity for p in plants.values() if p.status != "down")
    return {"total_available": total}


@app.post("/dispatch/", response_model=DispatchResponse)
def dispatch(request: DispatchRequest):
    """Allocate power demand across active plants based on capacity."""
    available = [(p.id, p.max_capacity) for p in plants.values() if p.status != "down"]
    if not available:
        return DispatchResponse(
            allocations={}, total_dispatched=0.0, unmet_demand=request.demand
        )

    available.sort(key=lambda x: x[1], reverse=True)
    demand = request.demand
    allocations = {}

    for pid, cap in available:
        if demand <= 0:
            allocations[pid] = 0.0
        else:
            alloc = min(cap, demand)
            allocations[pid] = alloc
            demand -= alloc

    total_dispatched = request.demand - demand
    return DispatchResponse(
        allocations=allocations, total_dispatched=total_dispatched, unmet_demand=demand
    )
