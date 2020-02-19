
#!usr/local/bin python3


def lazy_sum(*nums):

    def sum1():

        return sum(nums)

    return sum1



print(lazy_sum(*[1,2,3])())


