import datetime

ls = list()


def complete_array(list):
    for number in range(0, 100000000):
        ls.append(number)

def find_element(list, key):
    for n in list:
        if n == key:
            return True
    
    return False

# It returns location of x in given array arr
def binarySearch(arr, low, high, x):
    while low <= high:
        mid = low + (high - low) // 2
        # Check if x is present at mid
        if arr[mid] == x:
            return mid
        # If x is greater, ignore left half
        elif arr[mid] < x:
            low = mid + 1
        # If x is smaller, ignore right half
        else:
            high = mid - 1
    # If we reach here, then the element
    # was not present
    return -1


    
complete_array(ls)
start = datetime.datetime.now()
print(binarySearch(ls, 0, len(ls) - 1, 960000))
# print(find_element(ls, 960000)) 
end = datetime.datetime.now()
diff = end - start
print(int(diff.total_seconds() * 1000))

