import yaml


class Linker(object):

    def __init__(self):
        self.config = None

    def load(self, filename):

        with open(filename, 'r') as config_file:
            self.config = yaml.safe_load(config_file)

        print(self.config)

    def validate(self):
        if not self.config:
            raise ValueError("Configuration can not be empty before validating")

        assert 'actions' in self.config.keys()

    @staticmethod
    def custom_import(name):
        components = name.split('.')
        mod = __import__(components[0])
        for comp in components[1:]:
            mod = getattr(mod, comp)
        return mod

    def link(self):

        previous = None

        for i, action in enumerate(self.config['actions']):
            print(action)
            imported_class = self.custom_import(action)
            concrete_class = imported_class()

            if previous:
                previous.set_next(concrete_class)
                concrete_class.set_previous(previous)

            previous = concrete_class

        head = previous.find_head()
        head.print_walk()
