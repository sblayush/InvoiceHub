class Singleton(type):
	_instances = {}

	def __call__(self, *args, **kwargs):
		if self not in Singleton._instances:
			Singleton._instances[self] = super(Singleton, self).__call__(*args, *kwargs)
		return Singleton._instances[self]
