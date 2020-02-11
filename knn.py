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


def evaluateAlgorithm(train, test, k, oFile):
    #distance = []
    count = 0
    for i in range(len(test)):
        test_values = test[i]
        distance = getDistance(test_values, train)
        distance.sort()

        prediction = getPrediction(distance, k)
        #oFile.write([str(x) + ',' for x in test_values] + ',' + prediction + '\n')
        List = [test_values, prediction]
        for list in List:
            oFile.write(str(list) + ',')

        oFile.write('\n')

        if prediction == test_values[-1]:
            count += 1

    oFile.write('accuracy : ' + str(count / len(test)) + '\n\n')
    return count / len(test)


if __name__ == '__main__':
    fileName = 'G:\\f drive\\1IIT\\5th semester\\dbms2\\iris.txt'
    oFile = open('out.txt', 'w')

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

    for i in range(numberOfFold):
        start = i * numberOfFold
        end = start + percent
        test = shuffledData[start : end]
        train = shuffledData[: start] + shuffledData[end-1:]
        #print(test)
        #print(train)
        accuracy.append(evaluateAlgorithm(train, test, k, oFile))

    print(accuracy)
    meanAccuracy = sum(accuracy) / len(accuracy)
    print('mean accuracy : ', meanAccuracy)

    file.close()
    oFile.close()




