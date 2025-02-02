from datetime import date

from pydantic import BaseModel, ConfigDict


class MembershipIn(BaseModel):
    valid_until: date
    name: str


class Membership(MembershipIn):
    model_config = ConfigDict(from_attributes=True)
    id: int
