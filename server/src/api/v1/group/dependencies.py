from src.core.exceptions import BadRequest

from ..vk.service import vk_service


async def validate_vk_domain(domain: str) -> str:
    """Confirm the group domain exists in VK."""
    if not await vk_service.is_group_real(domain):
        raise BadRequest("Group not found in VK")
    return domain
