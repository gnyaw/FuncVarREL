import json

class FUNC:
    def __init__(self, name, desc=""):
        self.name = name
        self.desc = desc
        self.vars = {
            "intern": [],
            "extern": []
        }

    def add_var(self, var, intern_or_extern):
        self.vars[intern_or_extern].append(var)
        var.funcs[intern_or_extern].append(self)
    

class FUNCS:
    def __init__(self):
        self.funcs = []

    def new_func(self, name, desc=""):
        f = FUNC(name, desc)
        self.funcs.append(f)
        return f
    
    def __iter__(self):
        return iter(self.funcs)
    
    def __getitem__(self, key):
        return self.funcs[key]

 
class VAR:
    def __init__(self, name, desc=""):
        self.name = name
        self.desc = desc
        self.funcs = {
            "intern": [],
            "extern": []
        }

    def add_to_func(self, func, intern_or_extern):
        func.vars[intern_or_extern].append(self)
        self.funcs[intern_or_extern].append(func)

    def __str__(self) -> str:
        return self.name

class VARS:
    def __init__(self):
        self.vars = []

    def new_var(self, name, desc=""):
        v = VAR(name, desc)
        self.vars.append(v)
        return v

    def __iter__(self):
        return iter(self.vars)
    


class SPACE:
    def __init__(self, name, parent=None):
        self.name = ""
        self.parent = parent
        self.children = []
        self.funcs = FUNCS()
        self.vars = VARS()

    def show(self):
        from pprint import pprint
        for f in self.funcs:
            pprint(f.__dict__)
        for v in self.vars:
            pprint(v.__dict__)


def _serializable_rep(self, debug=False):
    if not debug:
        def print(*args, **kwargs):
            pass
    print("On:", self, "ObjectType:", type(self))
    if hasattr(self, "__dict__") or type(self) == dict:
        try:
            iter_dict = self.__dict__
        except:
            iter_dict = self
        serializable_obj = {}
        print("has dict")
        for key in iter_dict:
            print("Serializing:", key)
            obj = iter_dict[key]
            try:
                json.dumps(obj)
                serializable_obj[key] = obj
                print("==>OK")
            except:
                print("==>NG")
                serializable_obj[key] = _serializable_rep(obj)
    elif type(self) == list:
        serializable_obj = []
        print("is list")
        for item in self:
            print("Serializing:", item)
            try:
                json.dumps(item)
                serializable_obj.append(item)
                print("==>OK")
            except:
                print("==>NG")
                input("continue?")
                serializable_obj.append(_serializable_rep(item))
    else:
        print("unknown type error")
    return serializable_obj


def serializable(self, debug=False):
    print("Serialize start!")
    obj = _serializable_rep(self, debug)
    print("Serialize end!")
    return obj
    



space = SPACE("test space")

var1 = space.vars.new_var("var1")
func1 = space.funcs.new_func("func1")

func1.add_var(var1, "intern")

print(serializable(space))

