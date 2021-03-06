from warp import runtime


def allowed(avatar, obj):
    if avatar is None:
        roles = (runtime.config['roles'][x]
                 for x in runtime.config.get('defaultRoles', []))
    else:
        roles = avatar.roles

    for role in roles:
        opinion = role.allows(obj)
        if opinion is not None:
            return opinion

    return False


# ---------------------------


class Role(object):
    def __init__(self, ruleMap, default=[]):
        self.ruleMap = ruleMap
        self.default = default

    def allows(self, obj):
        if obj in self.ruleMap:
            rules = self.ruleMap[obj]
        else:
            rules = self.default
            
        for rule in rules:
            opinion = rule.allows(obj)
            if opinion is not None:
                return opinion


# ---------------------------

class Combine(object):
    combiner = None

    def __init__(self, *checkers):
        self.checkers = checkers

    def allows(self, other):
        return self.combiner(c.allows(other) for c in self.checkers)
    

class All(Combine):
    combiner = all

class Any(Combine):
    combiner = any

# ---------------------------


class Equals(object):

    def __init__(self, key):
        self.key = key
    
    def allows(self, other):
        return self.key == other


class Callback(object):

    def __init__(self, callback):
        self.callback = callback

    def allows(self, other):
        return self.callback(other)



# ---------------------------


class Allow(object):    
    def allows(self, other):
        return True


class Deny(object):
    def allows(self, other):
        return False
