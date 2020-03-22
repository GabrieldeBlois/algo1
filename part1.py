import numpy as np
import math

# way faster thanks to the use of searchsorted
def find_nearest_sorted(array,value):
    idx = np.searchsorted(array, value, side="left")
    if idx > 0 and (idx == len(array) or math.fabs(value - array[idx-1]) < math.fabs(value - array[idx])):
        return idx-1
    else:
        return idx

def greedy_nearestHeuristic(houseArray, currentPosValue):
    heuristicArray = np.array(houseArray)
    for i in range(len(heuristicArray)):
        score = abs(houseArray[i] - currentPosValue)
        heuristicArray[i] = score
    return heuristicArray

# this only goes to the closest house without looking further 
def greedy_withHeuristic(houseArray, heuristicFunc):
    # let's sort the array for optimization matter
    # numpy uses a mergesort https://docs.scipy.org/doc/numpy/reference/generated/numpy.sort.html
    # which is O(n * log(n))
    houseArray = np.sort(houseArray)
    
    # the snow machine does not begin at index 0 but at value 0.
    # We must find the index of the value 0
    currentPos = 0    

    result = []
    while len(houseArray) > 0:

        # calculating the heuristic for this iteration
        heuristicArray = heuristicFunc(houseArray, currentPos)
        
        # looking for the minimal value of the heuristic function result: O(n)
        minHeuristicValue = np.amin(heuristicArray)
        minIdx = np.where(heuristicArray == minHeuristicValue)[0][0]
        minValue = houseArray[minIdx]
        
        # now we need to reach the minValue position
        # by passing by all the values between currentPos and minValue
        drivingIdx = find_nearest_sorted(houseArray, currentPos)
        if minValue > currentPos:
            if houseArray[drivingIdx] < currentPos:
                drivingIdx += 1
        elif minValue < currentPos:
            if houseArray[drivingIdx] > currentPos:
                drivingIdx -= 1
            
        
        # check if we are going left or right
        negRet = (1, -1)[drivingIdx > minIdx]
        
        # going left or right, and adding the houses to the result set
        rangeToGo = range(drivingIdx, minIdx + negRet, negRet)
        # print(rangeToGo)
        for i in rangeToGo:
            result.append(houseArray[i])
            
        # creating a mask to delete all the houses we have came through
        houseToDeleteMask = np.full((len(houseArray)), True)

        houseToDeleteMask[rangeToGo] = False
        
        # deleting the houses we have been on
        houseArray = houseArray[houseToDeleteMask]
        
        # setting currentPos for the next loop iteration
        currentPos = minValue
        
    return result

def parcours(houseList):
    return greedy_withHeuristic(houseList, greedy_nearestHeuristic)