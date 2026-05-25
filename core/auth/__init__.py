from fastapi.params import Depends
from typing import Annotated

from core.config.jwt_config import get_current_user, get_is_admin

user_dependency = Annotated[dict, Depends(get_current_user)]
admin_dependency = Annotated[bool, Depends(get_is_admin)]
