from typing import NamedTuple


class Address(NamedTuple):
    host: str
    port: int

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self)

    def __str__(self):
        return '%s:%s' % (self.host, self.port)
