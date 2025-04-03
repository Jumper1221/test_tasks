lst = [1, 2, 3, 45, 356, 569, 600, 705, 923]


def search(number: int, lst: list) -> bool:
    left, right = 0, len(lst) - 1

    while left <= right:
        mid = (left + right) // 2
        if number == lst[mid]:
            return True
        elif number > lst[mid]:
            left = mid + 1
        else:
            right = mid - 1
    return False


print(search(45, lst))
