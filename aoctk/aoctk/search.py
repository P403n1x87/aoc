def bisect(search_space: list, cond: callable) -> int:
    """Binary search

    Bisects the linear search space for the point where the condition flips.
    """
    if not search_space:
        raise ValueError("Empty search space")

    lo, hi = 0, len(search_space) - 1
    cond_lo, cond_hi = cond(search_space[lo]), cond(search_space[hi])

    if cond_lo == cond_hi and len(search_space) > 1:
        raise ValueError("Condition does not flip on search space bounds")

    while lo < hi:
        if cond(search_space[mid := (lo + hi) // 2]) == cond_lo:
            lo = mid + 1
        else:
            hi = mid

    return lo
