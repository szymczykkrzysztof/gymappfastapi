import logging

from fastapi import APIRouter, HTTPException

from gymappapi.database import membership_table, database
from gymappapi.models.membership import Membership, MembershipIn

router = APIRouter()
logger = logging.getLogger(__name__)


async def find_membership(membership_id: int):
    query = membership_table.select().where(membership_table.c.id == membership_id)
    return await database.fetch_one(query)


async def delete_membership(membership_id: int):
    query = membership_table.delete().where(membership_table.c.id == membership_id)
    logger.debug(query)
    return await database.execute(query)


@router.get("/membership", response_model=list[Membership])
async def get_all_memberships():
    query = membership_table.select()
    logger.debug(query)
    return await database.fetch_all(query)


@router.post("/membership", response_model=Membership, status_code=201)
async def create_membership(post: MembershipIn):
    data = post.model_dump()
    query = membership_table.insert().values(data)
    logger.debug(query)
    last_record_id = await database.execute(query)
    return {**data, "id": last_record_id}


@router.get("/membership/{membership_id}", response_model=Membership)
async def get_membership(membership_id: int):
    membership = await find_membership(membership_id)
    if not membership:
        raise HTTPException(status_code=404, detail="Membership not found")
    return membership


@router.delete("/membership/{membership_id}", status_code=204)
async def delete_membership(membership_id: int):
    membership = await find_membership(membership_id)
    if not membership:
        raise HTTPException(status_code=404, detail="Membership not found")
    query = membership_table.delete().where(membership_table.c.id == membership_id)
    logger.debug(query)
    await database.execute(query)
    return {}
