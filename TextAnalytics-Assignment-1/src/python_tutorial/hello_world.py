import os, datetime

print("@global is initialized the file is run or load: Hello, World!")

# PEP8 Code convention: https://peps.python.org/pep-0008/#global-variable-names 
# It is BAD to use the same name for global and local variable
# DO NOT DO THIS. As it will also impact other files import this module.
# How to write pythonic code: https://builtin.com/data-science/pythonic#:~:text=Pythonic%20is%20a%20term%20used,and%20not%20deciphering%20existing%20code. 
case_sensitive = True

def say_helloworld(case_sensitive: bool = False):
    print(f"@say_hello: {hello_str(case_sensitive)}, {world_str(case_sensitive)}!")

def hello_str(case_sensitive: bool = False):
    if case_sensitive:
        return "Hello"
    else:
        return "hello"

def world_str(case_sensitive: bool = False):
    if case_sensitive:
        return "World"
    else:
        return "world"
    
def time_decorator(func):
    def wrapper(*args, **kargs):
        print("================================================")
        print(f"BeforeSay:{datetime.datetime.now().timestamp()}")
        func(*args, **kargs)
        print(f"AfterSay: {datetime.datetime.now().timestamp()}")
        print("================================================")
    return wrapper

class Base(object):
    def __init__(self):
        print("Base Init")

    def say(msg: str):
        print(f"{msg}")

class SayOnce(Base):

    @staticmethod
    @time_decorator
    def callFuncSay(case_sensitive: bool, func):
        print("using are using callFunc_say:\n")
        func(case_sensitive)

    @staticmethod
    @time_decorator
    def passArgSay(case_sensitive: bool, msg: str):
        if not case_sensitive:
            msg = msg.lower()
        print(f"using are using passArg_say:\n{msg}")

    def __init__(self, case_sensitive: bool):
        self.case_sensitive = case_sensitive
        super().__init__()

    def say(self, msg: str = ""):
        SayOnce.passArgSay(self.case_sensitive, msg)

    def do(self, func):
        SayOnce.callFuncSay(self.case_sensitive, func)

 # You cannot have mulitple functions with the same name and different signatures.
    # def say(func):
    #     SayOnce.callFuncSay(func)

class SayNTimes(Base):

    # higher-order static method
    @staticmethod
    @time_decorator
    def callFuncSay(N: int, case_sensitive: str, func):
        print(f"using are using callFunc_say for {N} times (case_senstive={case_sensitive}):\n")
        for i in range(1, N+1):
            func(case_sensitive)

    # higher-order static method
    @staticmethod
    @time_decorator
    def passArgSay(N: int, case_sensitive: str, msg: str):
        if not case_sensitive:
            msg = msg.lower()
        print(f"using are using passArg_say for {N} times (case_senstive={case_sensitive}):")
        for i in range(1, N+1):
            print(msg)

    def __init__(self, N_times: int, case_sensitive: bool):
        # without self, it is just a local variable in the __init__ function
        # n_times = N_times
        self.n_times = N_times
        self.case_sensitive = case_sensitive
        super().__init__()
        #Base.__init__(self, case_sensitive)

    def say(self, msg: str = ""):
        SayNTimes.passArgSay(self.n_times, self.case_sensitive, msg)

    def do(self, func):
        SayNTimes.callFuncSay(self.n_times, self.case_sensitive, func)

def main():
    # You don't have to have a main function
    # But it recommended for easier organization
    print("Main functon")
    sayOnce_sensitive = SayOnce(case_sensitive=True)
    sayNTime_insensitive = SayNTimes(N_times=3, case_sensitive=False)

    sayOnce_sensitive.say("Hello CS-5293 guys!")
    sayNTime_insensitive.say("Hello CS-5293 students!")
    sayNTime_insensitive.do(say_helloworld)

if __name__ == "__main__":
    # This is recommended when you code will both get executed directly or imported as modules.
    # to enter this branch: The script should be ran directly, not via a module
    # python hello_world.py will trigger this.
    # python -m hello_word.py will not tigger this.
    main()
