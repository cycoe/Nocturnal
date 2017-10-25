from numpy import *
import operator


def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(dataSet.shape)
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals, (m, 1))
    normDataSet /= tile(ranges, (m, 1))
    return normDataSet, ranges, minVals


def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0] #shape函数用来读取矩阵的维的长度，返回值为(4L,2L)
    diffMat = tile(inX, (dataSetSize, 1)) - dataSet #tile函数用来重复 A=[1,2] tile(A,(2,3)) -> [[1,2,1,2，1,2], [1,2,1,2,1,2]]
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5

    sortedDistIndicies = distances.argsort()
    classCount = {}
    for i in range(k):
        votedLabel = labels[sortedDistIndicies[i]]
        classCount[votedLabel] = classCount.get(votedLabel, 0) + 1 #dict.get(key, default_value)函数用来取键对应的值，若键不存在则值为defalut_vlaue
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True) #operator.itemgetter(1)表示根据多级列表的第二个元素进行排序
    return sortedClassCount[0][0]


def file2Matrix(filename):
    with open(filename) as fr:
        arrayOLines = fr.readlines()
    numberOfLines = len(arrayOLines)
    returnMat = zeros((numberOfLines, 3)) #注意两个括号

    classLabelVector = []
    index = 0
    for line in arrayOLines:
        line = line.strip() #删除开头和结尾处的空白符
        listFromLine = line.split('\t')
        returnMat[index, :] = listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index += 1
    return returnMat, classLabelVector
