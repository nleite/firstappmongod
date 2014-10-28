import inspect
class Account(object):

    def __init__(self, parser):
        if inspect.isclass(parser):
            self.parser = parser
        else: 
            raise TypeError('Incorrect type for `parser` object: Expecting class object')

    def parse_document(self, document):
        return self.parser().parse(document)

