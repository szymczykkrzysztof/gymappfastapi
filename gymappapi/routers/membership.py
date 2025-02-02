from fastapi import APIRouter

from gymappapi.database import membership_table, database
from gymappapi.models.membership import Membership, MembershipIn

router = APIRouter()


@router.get("/membership", response_model=list[Membership])
async def get_all_memberships():
    query = membership_table.select()
    return await database.fetch_all(query)


@router.post("/membership", response_model=Membership, status_code=201)
async def create_membership(post: MembershipIn):
    data = post.model_dump()
    query = membership_table.insert().values(data)
    last_record_id = await database.execute(query)
    return {**data, "id": last_record_id}
