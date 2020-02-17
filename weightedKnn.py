from random import shuffle

def getDistance(test, train):
    test = test[:len(test)-1]
    distance = []

    for training in train:
        x = 0
        for i in range(len(test)):
            x += (float(test[i]) - float(training[i])) ** 2
        #print(training)
        distance.append([x ** .5, training[-1]])

    return distance


def getPrediction(distance, k):
    output_values = [dist[-1] for dist in distance[:k]]
    prediction = max(set(output_values), key=output_values.count)
    return prediction


def weightedKnn(distance, k):
    output_values = [dist[-1] for dist in distance[:k]]
    output_values = set(output_values)
    output_values = list(output_values)

    values = set(map(lambda x: x[1], distance))
    new_list = [[y[0] for y in distance if y[1] == x] for x in values]

    weight = []
    myWeight = []

    for i in range((len(output_values))):
        sum = 0.0
        wSum = 0.0
        for j in new_list[i]:
            sum += 1.0 / (j + 1e-10)
            wSum += 1.0 / (j**2 + 1e-10)

        weight.append(sum)
        myWeight.append(len(new_list[i]) * sum)

    index = weight.index(max(weight))
    wIndex = myWeight.index(max(myWeight))

    return output_values[index], output_values[wIndex]


def writeInFile(List, wList, mList):
    for list in List:
        oFile.write(str(list) + ',')

    oFile.write('\n')

    for list in wList:
        woFile.write(str(list) + ',')

    woFile.write('\n')

    for list in mList:
        moFile.write(str(list) + ',')

    moFile.write('\n')


def evaluateAlgorithm(train, test, k, oFile, woFile, moFile):
    #distance = []
    count = 0
    wCount = 0
    mCount = 0
    for i in range(len(test)):
        test_values = test[i]
        distance = getDistance(test_values, train)
        distance.sort()

        prediction = getPrediction(distance, k)
        mPrediction, wPrediction = weightedKnn(distance, k)
        #oFile.write([str(x) + ',' for x in test_values] + ',' + prediction + '\n')
        List = [test_values, prediction]
        wList = [test_values, wPrediction]
        mList = [test_values, mPrediction]
        writeInFile(List, wList, mList)




        print(prediction + ' ' + test_values[-1])

        if prediction == test_values[-1]:
            count += 1

        if wPrediction == test_values[-1]:
            wCount += 1

        if mPrediction == test_values[-1]:
            mCount += 1

    oFile.write('accuracy : ' + str(count / len(test)) + '\n\n')
    woFile.write('accuracy : ' + str(wCount / len(test)) + '\n\n')
    moFile.write('accuracy : ' + str(mCount / len(test)) + '\n\n')
    print('\n')

    return count / len(test), wCount / len(test), mCount / len(test)


if __name__ == '__main__':
    fileName = 'G:\\5 th semester\\dbms2\\knn\\iris.txt'
    oFile = open('outIris.txt', 'w')
    woFile = open('weight.txt', 'w')
    moFile = open('mWeight.txt', 'w')

    file = open(fileName, 'r')
    lines = file.readlines()
    numberOfLines = len(lines)
    print(numberOfLines)

    data = []
    i = 0
    for line in lines:
        values = line.split(',')
        data.append(values)
        i += 1

    shuffle(data)
    shuffledData = list.copy(data)
    #print(data)

    numberOfFold = int(input("number of fold: "))
    k = int(input('value of k: '))
    percent = int(len(shuffledData) / numberOfFold)
    accuracy = []
    wAccuracy = []
    mAccuracy = []

    for i in range(numberOfFold):
        start = i * percent
        end = start + percent
        test = shuffledData[start : end]
        train = shuffledData[: start] + shuffledData[end-1:]
        #print(test)
        #print(train)
        neutral, weight, mWeight = evaluateAlgorithm(train, test, k, oFile, woFile, moFile)
        accuracy.append(neutral)
        wAccuracy.append(weight)
        mAccuracy.append(mWeight)

    print(accuracy)
    meanAccuracy = sum(accuracy) / len(accuracy)
    print('mean accuracy : ', meanAccuracy)

    print(wAccuracy)
    w_meanAccuracy = sum(wAccuracy) / len(wAccuracy)
    print('weighted mean accuracy : ', w_meanAccuracy)

    print(mAccuracy)
    m_meanAccuracy = sum(mAccuracy) / len(mAccuracy)
    print('weighted mean accuracy : ', m_meanAccuracy)

    file.close()
    oFile.close()
    woFile.close()
    moFile.close()




