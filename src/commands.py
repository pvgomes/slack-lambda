class Command:
    def execute(self):
        raise NotImplementedError("Commands must implement execute")

class Help(Command):
    def execute(self):
        return '''
            This is the help
        '''

class Query(Command):
    def execute(self):
        return 'Executing query in some place'


class Wiki(Command):
    pass
