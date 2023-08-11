# from uuid import UUID
# from menu_app.cache.cache_base import CacheBase


# class CacheInvalidation(CacheBase):
#     async def menu_cache_invalidation(self, menu_id):
#         await self.del_list(prefix='Menus')
#         await self.delete_cache(menu_id=menu_id)
#         await self.del_list(prefix='Menus')
#         await self.del_list(prefix=f'Submenus:{menu_id}')
#         await self.delete(menu_id=menu_id)
#         await self.del_child(parent_id=menu_id)

#     async def submenu_cache_invalidation(self, menu_id: UUID, submenu_id: UUID):
#         await self.del_list(prefix=f'Submenus:{menu_id}')
#         await self.del_all_lists(menu_id=menu_id)
#         await self.delete(menu_id=menu_id)
#         await self.delete_cache(menu_id=menu_id, submenu_id=submenu_id)
#         await self.del_all_lists(menu_id=menu_id, submenu_id=submenu_id)
#         await self.delete(menu_id=menu_id)
#         await self.delete(menu_id=menu_id, submenu_id=submenu_id)
#         await self.del_child(parent_id=submenu_id)

#     async def dish_cache_invalidation(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID):
#         await self.del_all_lists(menu_id=menu_id, submenu_id=submenu_id)
#         await self.delete(menu_id=menu_id)
#         await self.delete(menu_id=menu_id, submenu_id=submenu_id)
#         await self.del_list(prefix=f'Dishes:{submenu_id}:{menu_id}')
#         await self.del_all_lists(menu_id=menu_id, submenu_id=submenu_id)
#         await self.delete(menu_id=menu_id)
#         await self.delete(menu_id=menu_id, submenu_id=submenu_id)
#         await self.delete(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
