
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.classes.swarm_management import SwarmManagement

router = APIRouter()
swarmManagement = SwarmManagement()

@router.post("/swarm/interact")
async def interact_with_swarm(query: str):
    """
    Interact with the specified Swarm agent.
    """
    response = swarmManagement.make_query(query=query)
    return JSONResponse(content=response, status_code=status.HTTP_200_OK)