from typing import Optional


def page_size(size: Optional[int], default: int, maximum: int) -> int:
    if size is None:
        return default
    return max(1, min(size, maximum))


def offset_limit(page: int, size: int) -> tuple[int, int]:
    p = max(1, page)
    return (size * (p - 1), size)
