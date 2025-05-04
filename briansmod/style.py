import ast, string, os, time

class WTFYouOnAbout(Exception):
    def __init__(self, filename, key, val):
        super().__init__("Your theme " + filename + " tries to say " + key + " should be " +
                         val + ", but I have no clue what that is. Fix it!")

def parsetheme(filename):
    result = {}
    current_block = None
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('//'):
                continue  # skip empty lines and comments
            if line.endswith('{'):
                current_block = line[:-1].strip()
                result[current_block] = {}
            elif line == '}':
                current_block = None
            elif current_block:
                if ':' in line:
                    key, val = line.split(':', 1)
                    key = key.strip()
                    val = val.strip().rstrip(';')
                    print("DEBUG-----------> val = " + val)
                    if val[0] in string.ascii_letters: #assume its a previously assigned var
                        if val in result[current_block].keys():
                            result[current_block][key] = result[current_block][val]
                        elif val in result.keys():
                            result[current_block][key] = result[val]
                    else:
                        result[current_block][key] = ast.literal_eval(val)
            elif line[0] in string.ascii_letters:
                key, val = line.split(':', 1)
                key = key.strip()
                val = val.strip().rstrip(';')
                if key in result:
                    print("\nbriansmod.style Warning: " + key + " defined twice in theme " + filename + ".\n")
                else:
                    if val[0] in string.ascii_letters:
                        if val in result.keys():
                            result[key] = result[val]
                        else: raise WTFYouOnAbout(filename, key, val)
                    else:
                        print("DEBUG------------> val = " + val)
                        result[key] = ast.literal_eval(val)
    return result

def themepath(themename):
    configpath = os.getenv("$XDG_CONFIG_HOME")
    if configpath is None:
        return os.path.expanduser("~/.config/qtile/" + themename)
    else:
        return configpath + "/qtile/" + themename

class Theme:
    def __init__(self):
        return

def LoadTheme( themefile):
    themefile = themepath(themefile)
    theme = parsetheme(os.path.expandvars(themefile))
    time.sleep(1) #accessing config too early raises AttributeError
    result = Theme()
    try:        
        for attr in theme.keys():
            if '.' in attr:
                print("DEBUG-----> " + attr)
                namelist = attr.split('.')
                namelist.reverse()
                target = result
                while len(namelist) > 1:
                    nm = namelist.pop()
                    if '[' in nm:
                        idnm, idex = nm.split('[')
                        idex = ast.literal_eval(idex.rstrip(']'))
                        target = getattr(target, nm)[idex]
                    else:
                        target = getattr(target, nm)
                nm = namelist.pop()
                if '[' in nm:
                    idnm, idex = nm.split('[')
                    idex = ast.literal_eval(idex.rstrip(']'))
                    getattr(target, idnm)[idex] = theme[attr]
                else:
                    setattr(target, nm, theme[attr])
            else:
                if '[' in attr:
                    idnm, idex = attr.split('[')
                    idex = ast.literal_eval(idex.rstrip(']'))
                    getattr(result, idnm)[idex] = theme[attr]
                else:
                    setattr(result, attr, theme[attr])
    except IndexError: raise IndexError("Your theme file dun goofed and tried to index " + 
                                        "out of bounds of a list. Fix it!")
    return result

