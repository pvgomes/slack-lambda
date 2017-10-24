class Command:
    def execute(self, argument):
        raise NotImplementedError("Commands must implement execute")

class Help(Command):
    def execute(self, argument):
        return 'This is the help with argument %s' % argument

class Query(Command):
    def execute(self, argument):
        return 'Executing query in some place with argument %s ' % argument


class Wiki(Command):
    pass
