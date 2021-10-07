import os
from hashlib import md5
from datetime import datetime


def generate_str_hash(path):
    with open(path, 'rb') as f:
        current_file = f
        while True:
            current_line = current_file.readline()
            if not current_line:
                break
            line_hash = md5(current_line).hexdigest()
            yield line_hash

def logger_decor_fabric(log_target):
    def logger_decor(old_function):
        def new_function(*args, **kwargs):
            start_time = datetime.now()
            result = old_function(*args, **kwargs)
            log_arg = ""
            for arg in [args, kwargs]:
                log_arg += str(arg).strip("{").strip("}").strip("(").strip(")").strip(",")
            log_string = f"{start_time} function: {new_function.__name__}({log_arg}) has result {result}"
            if os.path.isfile(log_target):
                mode_flag = "a"
            else:
                mode_flag = "w"
            with open(log_target, mode_flag) as fl:
                fl.write(log_string + "\n")
                result = fl
            print(log_string)
            return result
        new_function.__name__ = old_function.__name__
        return new_function
    return(logger_decor)

@logger_decor_fabric("log_target")
def interface(raw, code_target, mark, b=30):
    '''  Принимает путь code_target к файлу, строки которого будут кодироваться и
     записываться в code_target = "md5_code.txt"

    '''
    mark_str = mark * b + "function started" + mark * b
    print(mark_str)
    if os.path.exists(code_target):
        with open(code_target, "w+") as f:
            f.seek(0)
    for i in generate_str_hash(raw):
        if os.path.isfile(code_target):
            mode_flag = "a"
        else:
            mode_flag = "w"
        with open(code_target, mode_flag) as fl:
            fl.write(i + "\n")
            result = fl
    return result

tobe_encoded = "D:\\netology\\text.txt"
a = interface(tobe_encoded, "md5_code.txt", "!", 50)
print(a)

