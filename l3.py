
i = 0

def createCounter():

    i = 0

    def counter():

        return  i+1

    return counter


f = createCounter()

print(f(),f()) # 1,2

