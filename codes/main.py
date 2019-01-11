from dm import dm
import random

input = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
indexList = [0, 1, 2, 3, 4, 5, 6, 7, 8 ,9]
inputIndex = random.sample(indexList, 5)
for i in range(5):
    input[inputIndex[i]] = 1


matcher = dm(10, 10, 3, [0.3, 0.3, 0.4])
matcher.attributes()
matcher.initialization()
print('input: ', end = '')
print(input)
output = matcher.encoding(input)
print('output: ', end = '')
print(output)
input = matcher.decoding(output)
print('After decoding: ', end = '')
print(input)

