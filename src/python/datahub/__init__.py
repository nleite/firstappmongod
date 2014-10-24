class Account(object):

	def __init__(self, parser):
		self.parser = parser

	def parse_document(self, document):
		return self.parser.parse()

