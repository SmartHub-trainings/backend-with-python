# def divide(a,b):
#     return a/b


# print(divide(4,2))
# print(divide(3,9))

# def do_3_times(func):
#     for i in range(3):
#         func()
        
# def say_hello():
#     print("hello")
    
# say_hello()

# do_3_times(say_hello)


#currying
# def add_1(a):
#     def add_again(b):
#         return a+b
#     return add_again
    
    
# # print(add_1(4)(8))

# funct1= add_1(6)
# result = funct1(12)
# print(result)






#closure
def decorate(func):
    def inner(x,y):
        print("before decorating")
        if x<y:
            x,y = y,x
        result =func(x,y)
        print("after decorating")
        return result
    return inner
@decorate
def divide(a,b):
    return a/b
# divide1 = decorate(divide)
# divide1(1,2)
# divide1(3,4)
# divide = decorate(divide)
# print(divide(1,2))
# print(divide(3,4))
    
    
    
    


