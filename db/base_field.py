class BaseFieldDescriptor(object):
    def __set_name__(self, owner, name):
        raise NotImplementedError

    def __get__(self, instance, owner):
        raise NotImplementedError

    def __set__(self, instance, value):
        raise NotImplementedError

    def _validate(self, *args, **kwargs):
        raise NotImplementedError
