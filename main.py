import  threading
import concurrent.futures
import time


class MyVar:

    def __init__(self) -> None:
        self._value = 0
        self._tmp = None

    def update(self, number): 
       
        self._tmp = self._value
        self._tmp = number
        time.sleep(0.1)
        self._value = self._tmp




def acces_to_this_var():
    pass

def my_func(number, obj: MyVar):
    for x in range(number):
        obj.update(x)
        time.sleep(1)


running = True
local_obj = MyVar()
while running:
    print("----")
    print("Select options:")
    print("----")
    print("Finish program: 1")
    print("Start new thread: 2")
    print("Stop Thread: 3")
    print("Give me all thread running: 4")
    print("Get number from variable: 5")
    print("----")
    opt = input("Your option: ")

    if opt == "1":
        running = False
        print("Program finalized")
    elif opt == "2":
        _input_number = input("Put number to count in thread: ")
        t = threading.Thread(target=my_func, name=f"Count to {_input_number}", args=[int(_input_number), local_obj])
        t.start()
    elif opt == "3":
        _num = input("Put number of thread to count:")
        for th in threading.enumerate():
            if th.name.find(_num) > 0:
                print("finish this thread:", th)
                th.join()
    elif opt == "4":
        print(threading.enumerate())
    elif opt == "5":
        print(local_obj._value)
    else:
        print('doesnt exist')


with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
    ex.map()