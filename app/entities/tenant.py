from datetime import datetime, date
from typing import Optional


class TenantEntity:
    """
    Tenant Entity - Ingredients (data structures).

    Represents a person living in a PG room.
    Optionally linked to a User account for login access.
    """

    STATUS_OPTIONS = ["active", "checked_out", "on_notice"]
    ID_PROOF_TYPES = ["aadhar", "passport", "driving_license", "voter_id", "other"]

    def __init__(
        self,
        id: Optional[int] = None,
        user_id: Optional[int] = None,          # FK to users (optional login account)
        room_id: Optional[int] = None,          # FK to rooms (currently assigned room)
        first_name: str = "",
        last_name: str = "",
        phone: str = "",
        alternate_phone: Optional[str] = None,
        email: Optional[str] = None,
        permanent_address: Optional[str] = None,
        emergency_contact_name: Optional[str] = None,
        emergency_contact_phone: Optional[str] = None,
        id_proof_type: Optional[str] = None,
        id_proof_number: Optional[str] = None,
        move_in_date: Optional[date] = None,
        move_out_date: Optional[date] = None,
        deposit_amount: float = 0.0,
        status: str = "active",
        is_active: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.user_id = user_id
        self.room_id = room_id
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.alternate_phone = alternate_phone
        self.email = email
        self.permanent_address = permanent_address
        self.emergency_contact_name = emergency_contact_name
        self.emergency_contact_phone = emergency_contact_phone
        self.id_proof_type = id_proof_type
        self.id_proof_number = id_proof_number
        self.move_in_date = move_in_date
        self.move_out_date = move_out_date
        self.deposit_amount = deposit_amount
        self.status = status
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def has_login(self) -> bool:
        """Check if this tenant has a linked login account."""
        return self.user_id is not None

    @property
    def is_currently_staying(self) -> bool:
        return self.status == "active"

    def checkout(self, checkout_date: date) -> None:
        self.status = "checked_out"
        self.move_out_date = checkout_date
        self.room_id = None

    def put_on_notice(self) -> None:
        self.status = "on_notice"

    def is_valid(self) -> bool:
        return bool(self.first_name and self.phone)
