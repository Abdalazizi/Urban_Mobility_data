def _partition(arr, low, high, key, descending):
    pivot_index = low
    pivot_value = arr[pivot_index][key]
    
    # Move pivot to the end to work with the rest of the array
    arr[pivot_index], arr[high] = arr[high], arr[pivot_index]
    
    store_index = low
    for i in range(low, high):
        if descending:
            if arr[i][key] > pivot_value:
                arr[i], arr[store_index] = arr[store_index], arr[i]
                store_index += 1
        else:
            if arr[i][key] < pivot_value:
                arr[i], arr[store_index] = arr[store_index], arr[i]
                store_index += 1
    
    # Move pivot back to its final sorted place
    arr[store_index], arr[high] = arr[high], arr[store_index]
    return store_index

def _quick_sort_recursive(arr, low, high, key, descending):
    if low < high:
        pi = _partition(arr, low, high, key, descending)
        _quick_sort_recursive(arr, low, pi - 1, key, descending)
        _quick_sort_recursive(arr, pi + 1, high, key, descending)

def manual_sort(data, key, descending=False):
    """
    Manually sorts a list of dictionaries using the Quick Sort algorithm.

    Args:
        data (list): A list of dictionaries to sort.
        key (str): The dictionary key to sort by.
        descending (bool): If True, sorts in descending order.

    Returns:
        list: The sorted list.
    """
    if not data:
        return []

    # Create a copy to avoid modifying the original list in place
    data_copy = list(data)
    
    _quick_sort_recursive(data_copy, 0, len(data_copy) - 1, key, descending)
    
    return data_copy
