from abc import abstractmethod, ABC

from sqlalchemy import select
from .models import Post, SiteUser


class AbstractRepository(ABC):

    @abstractmethod
    def insert(self):
        raise NotImplementedError


class PostRepository(AbstractRepository):
    def __init__(self):
        pass

    async def insert(self):
        pass


async def get_user(email: str = None, user_id: str = None) -> SiteUser:
    with SiteUser.session() as session:
        if email:
            return session.scalar(select(SiteUser).filter(SiteUser.email == email))
        if user_id:
            return session.scalar(select(SiteUser).filter(SiteUser.id == user_id))

