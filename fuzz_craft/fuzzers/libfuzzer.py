class Provider:
    def __init__(self, data=None):
        self._data = data

    def __repr__(self):
        raise NotImplementedError


class ConsumeIntegral(Provider):
    def __repr__(self):
        return f'provider.ConsumeIntegral<{self._data}>()'


class ConsumeFloatingPoint(Provider):
    def __repr__(self):
        return f'provider.ConsumeFloatingPoint<{self._data}>()'


class ConsumeBool(Provider):
    def __repr__(self):
        return 'provider.ConsumeBool()'
