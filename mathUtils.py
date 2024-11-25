def cumulSum(values):
    newVector = [values[0]]
    for i in range(1, len(values)):
        newVector.append(newVector[i - 1] + values[i])
    return newVector

#untested
def sortedBinarySearch(vector, value):
    begin = 0
    end = len(vector)
    while end != begin:
        middleIndex = (end - begin) / 2
        checkIndex = middleIndex + begin
        if value < vector[checkIndex]:
            end = middleIndex
        elif value == vector[checkIndex]:
            return checkIndex
        else:
            begin = middleIndex + 1
    return -1

def firstBiggerOrEqualsThan(vector, value):
    if vector[len(vector) - 1] < value:
        return -1
    for i in range (len(vector)):
        if vector[i] >= value:
            return i

def quantile25(vector):
    cumul = cumulSum(vector)
    quartile = cumul[len(cumul) - 1] / 4
    return firstBiggerOrEqualsThan(cumul, quartile)