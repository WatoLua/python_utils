def argmin(numberList):
    if not numberList:
        return None  # Retourne None si la liste est vide
    min_value = numberList[0]
    min_index = 0
    for i in range(1, len(numberList)):
        if numberList[i] < min_value:
            min_value = numberList[i]
            min_index = i
    return min_index

def getMinExcludingIndice(vector, indice):
    minValue = vector[0] + vector[1]
    minJ = -1
    for j in range(0, len(vector)):
        if indice != j and vector[j] < minValue:
            minValue = vector[j]
            minJ = j
    return j