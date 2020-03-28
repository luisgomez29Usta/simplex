# import numpy
#
# a = numpy.array([1, 2, 3, 4, 5, 6, 7, 8])
#
# print("A subset of array a = ", a[-3:])
#

import numpy

a = numpy.array([1, 2, 3, 4, 5])

# numpy.savetxt("myArray.csv", a)
# numpy.savetxt("myArray.csv", a,fmt='%.2f')

# for x in a[::-1]:
for x in reversed(a):
    print(x)

