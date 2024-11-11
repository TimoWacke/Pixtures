import math


digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9","10"]

def r(x):
    return (math.sqrt(2 * math.pi * x) * (x / math.e)**x)


def prop(n):
    bruch = r(z)/(r(z-n) * math.pow(z, n))
    return 1 - bruch

def add(x, y):
    rresult = ""
    if len(y) > len(x):
        temp = y[::-1]
        y = x[::-1]
        x = temp
    else:
        x = x[::-1]
        y = y[::-1]
    i = 0
    über = 0
    for a in x:
        d = digits.index(a) + über
        if len(y) > i:
            b = y[i]
            d += digits.index(b) 
        dstr = digits[d % len(digits)]
        über = d // len(digits)
        rresult = dstr + rresult
        i += 1

    if über != 0:
        rresult = digits[über] + rresult
    return rresult

def sub(x, y):
    rresult = ""
    if len(y) > len(x):
        return False
    x = x[::-1]
    y = y[::-1]
    i = 0
    über = 0
    for a in x:
        d = digits.index(a) + über
        if len(y) > i:
            b = y[i]
            d -= digits.index(b)
      
        dstr = digits[d % len(digits)]
        if d < 0:
            über = -1
        else:
            über = 0
        rresult = dstr + rresult
        i += 1
    if über < 0:
        return False
    for l in rresult[:-1]:
        if digits[0] == l:
            rresult = rresult[1:]
        else:
            break
    return rresult

def div(x, y):
    if not sub(x, y):
        return digits[0]
    return add(digits[1], div(sub(x,y), y)) 

def mul(x, y):
    if digits[0] == x or digits[0] == y:
        return digits[0]
    ret = digits[0]
    while x != digits[0]:
        ret = add(ret, y)
        x = sub(x, digits[1])
    return ret

def pow(x, y):
    if y == digits[0]:
        return digits[1]
    return pow(mul(x, pow(x, sub(y, digits[1]))))

def fac(x):
    if x == digits[0]:
        return digits[1]
    return mul(fac(sub(x, digits[1])), x)

def testAdd(x , y):
    expected = str(x + y)
    received = add(str(x), str(y))
    testOutput(expected, received, x, "+", y)


def testSub(x , y):
    expected = str(x - y)
    received = sub(str(x), str(y))
    testOutput(expected, received, x, "-", y)


def testDiv(x, y):
    expected = str(x // y)
    received = div(str(x), str(y))
    testOutput(expected, received, x, "//", y)


def testMul(x, y):
    expected = str(x * y)
    received = mul(str(x), str(y))
    testOutput(expected, received, x, "*", y)

def testFac(x):
    expected = str(math.factorial(x))
    received = fac(str(x))
    testOutput(expected, received, x, "!")


def testOutput(expected, received, x, operator, y=""):
    if expected == received:
        print(f'Test passed for {x} {operator} {y} = {expected}')
        print(f'-------------')
        return True
    else:
        print(f'Test failed for {x} {operator} {y}')
        print(f'expected {expected} received {received}')


import re

def giveCalcString(a, d, n):
    orginal = "1 - ( sqrt(2 * pi * (a^d)) * ((a^d) / e)^(a^d) / (sqrt(2 * pi * (a^d - n )) * ((a^d - n ) / e)^(a^d - n ) * (62^16)^n))"
    #1 - ( sqrt(2 * pi * (10^10)) * ((10^10) / e)^(10^10) / (sqrt(2 * pi * (10^10 - 1000 )) * ((10^10 - 1000 ) / e)^(10^10 - 1000 ) * (62^16)^1000))
     #1 - ( sqrt(2 * pi * (62^16)) * ((62^16) / e)^(62^16) / (sqrt(2 * pi * (62^16 - (10^9) )) * ((62^16 - (10^9) ) / e)^(62^16 - (10^9) ) * (62^16)^(10^9)))
    print(str(n) + "1")
    ret = re.sub('n', str(n), orginal)
    ret = re.sub('a', str(a), orginal)
    ret = re.sub('d', str(d), orginal)
    return ret

print(giveCalcString(62, 16, 10))