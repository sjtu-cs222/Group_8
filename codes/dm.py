import numpy
import threading

class dm:
    'distribution matcher'

    def __init__(self, k, n, M, pA):
        self.k = k
        # input_size. The input interval size is less than twice the output interval size
        self.n = n
        # output_size
        self.M = M
        # output_amplitude, The encoded symbols s will then be taken from the alphabet {1, 2, ... , M}
        self.pA = pA
        # empirical distribution on the output symbols
        bag = []
        # number of occurances of each output symbol

        self.inputBag = [0, 0]
        self.inputBag[0] = int(self.k / 2)
        self.inputBag[1] = self.k - self.inputBag[0]

        self.outputBag = [0] * len(self.pA)
        self.outputBag[len(self.pA) - 1] = self.n
        for i in range(len(self.pA) - 1):
            self.outputBag[i] = int(self.pA[i] * self.n)
            self.outputBag[len(self.pA) - 1] -= self.outputBag[i]
        
        self.inputInterval_symbol = [[]]
        self.inputInterval_size = [1]

        self.outputInterval_symbol = [[]]
        self.outputInterval_size = [1]

        self.mutex=threading.Lock()

    def attributes(self):
        print('input length: %d\noutput length: %d\nideal distribution: ' % (self.k, self.n), end = '')
        print(self.pA)

    def input_intervals(self):
        print(self.inputInterval_size)
        print(self.inputInterval_symbol)

    def output_intervals(self):
        print(self.outputInterval_size)
        print(self.outputInterval_symbol)

    def bags(self):
        print(self.inputBag)
        print(self.outputBag)

    def interval_partition(self, io, operationSample, bag):
        newBag = []
        flag = 0
        if io == 'input':
            self.mutex.acquire()
            operationIndex = self.inputInterval_symbol.index(operationSample)
            remain = 0
            for i in range(2):
                newBag.append(bag[i])
                if newBag[i] != 0:
                    remain += newBag[i]
            count = 0
            for i in range(2):
                if newBag[i] != 0:
                    flag = 1
                    count += 1
                    self.inputInterval_size.insert(operationIndex + count, self.inputInterval_size[operationIndex] * newBag[i] / remain)
                    self.inputInterval_symbol.insert(operationIndex + count, self.inputInterval_symbol[operationIndex] + [i])
            if flag == 1:
                self.inputInterval_size.pop(operationIndex)
                self.inputInterval_symbol.pop(operationIndex)
            count = -1
            self.mutex.release()
            for i in range(2):
                if newBag[i] != 0:
                    count += 1
                    newBag[i] -= 1
                    t = threading.Thread(target = self.interval_partition, args = (io, operationSample + [i], newBag))
                    t.setDaemon(True)
                    t.start()
                    t.join()
                    newBag[i] += 1

        if io == 'output':
            operationIndex = self.outputInterval_symbol.index(operationSample)
            remain = 0
            self.mutex.acquire()
            for i in range(self.M):
                newBag.append(bag[i])
                if newBag[i] != 0:
                    remain += newBag[i]
            count = 0
            for i in range(self.M):
                if newBag[i] != 0:
                    flag = 1
                    count += 1
                    self.outputInterval_size.insert(operationIndex + count, self.outputInterval_size[operationIndex] * newBag[i] / remain)
                    self.outputInterval_symbol.insert(operationIndex + count, self.outputInterval_symbol[operationIndex] + [i])
            if flag == 1:
                self.outputInterval_size.pop(operationIndex)
                self.outputInterval_symbol.pop(operationIndex)
            count = -1
            self.mutex.release()
            for i in range(self.M):
                if newBag[i] != 0:
                    count += 1
                    newBag[i] -= 1
                    t = threading.Thread(target = self.interval_partition, args = (io, operationSample + [i], newBag))
                    t.setDaemon(True)
                    t.start()
                    t.join()
                    newBag[i] += 1
        return
    
    def input_interval_produce(self):
        self.interval_partition('input', [], self.inputBag)

    def output_interval_produce(self):
        self.interval_partition('output', [], self.outputBag)

    def encoding(self, inputBits):

        index = self.inputInterval_symbol.index(inputBits)
        inputLower = 0
        for i in range(index):
            inputLower += self.inputInterval_size[i]

        outputLower = 0
        index2 = -1
        for i in range(len(self.outputInterval_symbol)):
            if outputLower >= inputLower:
                index2 = i
                break
            outputLower += self.outputInterval_size[i]
        if index2 == -1:
            print(outputLower)
            print('Encode failed.')
            return []
        return self.outputInterval_symbol[index2]

    def decoding(self, outputSymbols):
        index = self.outputInterval_symbol.index(outputSymbols)
        outputLower = 0
        for i in range(index):
            outputLower += self.outputInterval_size[i]

        inputLower = 0
        index2 = -1
        for i in range(len(self.inputInterval_symbol)):
            if inputLower >= outputLower:
                index2 = i - 1
                break
            inputLower += self.inputInterval_size[i]
        if index2 == -1:
            print(inputLower)
            print('Decode failed.')
            return []
        return self.inputInterval_symbol[index2]

    def initialization(self):
        print('Initializing distribution matcher')
        self.input_interval_produce()
        self.output_interval_produce()