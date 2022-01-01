import numpy
import matplotlib.pyplot as plot
import random

def numeric_diff(f, arg, index_of_var):
    h = 0.0001
    arg1 = arg.copy()
    arg2 = arg.copy()
    arg1[index_of_var] += h
    f1 = f(arg1)
    arg2[index_of_var] -= h
    f2 = f(arg2)
    return (f1 - f2) / (2 * h)


def function(arg):
    return arg[1] * arg[0] + arg[2]

#generate training set
limit = 500
#input:1 to 3
x = numpy.linspace(1, 4, limit)
#output:linear function
y0 = []
for i in range(0, limit):
    y0.append(function([x[i], 5, 3]) + random.random())

#linear regression: to find out the parameter 5
w1 = [0.1]
w2 = [0.1]
for i in range(0, limit):
    #actual output
    y = w1[i] * x[i] + w2[i]
    
    #arguments of function[input, parameter]
    arg = [x[i], w1[i], w2[i]]
    
    #delta w = learning factor * de/dw
    #Error function = 1/2 * (actual output - predicted output)
    #de/dw = de/dy * dy/dw(chain rule) 
    #de/dy = (actual output - predicted output)
    dydw1 = numeric_diff(function, arg, 1)
    dydw2 = numeric_diff(function, arg, 2)
    dedy = y - y0[i]
    deltaw1 = dedy * dydw1 * (1/limit)
    delatw2 = dedy * dydw2 * (1/limit)
    w1.append(w1[i] - deltaw1)
    w2.append(w2[i] - delatw2)

'''
plot.subplot(2,1,1)
plot.plot(w1)
plot.title("w1")
plot.subplot(2,1,2)
plot.plot(w2)
plot.title("w2")
'''
plot.plot(x, y0, '.')
plot.plot(x, w1[limit] * x + w2[limit])
plot.legend(["training set", "regression"])
plot.show()