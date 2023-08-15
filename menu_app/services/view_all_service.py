from fastapi import Depends

from menu_app.cache.cache_subjects import CacheViewAll
from menu_app.repositories.view_all_repository import ViewAllRepository
from menu_app.schemas import MenuAllOut


class ViewAllService:
    def __init__(self,
                 database_repository: ViewAllRepository = Depends()) -> None:
        self.database_repository = database_repository
        self.cache = CacheViewAll()

    async def get_all(self) -> list[MenuAllOut]:
        if await self.cache.check_list(prefix='ViewAll'):
            return await self.cache.load_list(prefix='ViewAll')
        result = await self.database_repository.get_all()

        await self.cache.save_list(subject=result, prefix='ViewAll')
        return result
