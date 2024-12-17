class DeployType(object):
    def __init__(self, key, name):
        self.key = key
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name