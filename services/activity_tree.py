from app.repositories.activity_repo import ActivityRepository


async def subtree_ids(repo: ActivityRepository, root_activity_id: int) -> list[int]:
    return await repo.list_children_ids_recursive(root_activity_id)
