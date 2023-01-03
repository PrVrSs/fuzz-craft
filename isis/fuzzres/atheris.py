class Provider:
    def __init__(self, data=None):
        self._data = data

    def __repr__(self):
        raise NotImplementedError


class ConsumeBytes(Provider):
    def __repr__(self):
        return f'ConsumeBytes({self._data})'


class ConsumeUnicode(Provider):
    def __repr__(self):
        return f'ConsumeUnicode({self._data})'


class ConsumeUnicodeNoSurrogates(Provider):
    def __repr__(self):
        return f'ConsumeUnicodeNoSurrogates({self._data})'


class ConsumeString(Provider):
    def __repr__(self):
        return f'ConsumeString({self._data})'


class ConsumeInt(Provider):
    def __repr__(self):
        return f'ConsumeInt({self._data})'


class ConsumeUInt(Provider):
    def __repr__(self):
        return f'ConsumeUInt({self._data})'


class ConsumeIntInRange(Provider):
    def __repr__(self):
        return f'ConsumeIntInRange({self._data})'


class ConsumeIntList(Provider):
    def __repr__(self):
        return f'ConsumeIntList({self._data})'


class ConsumeIntListInRange(Provider):
    def __repr__(self):
        return f'ConsumeIntListInRange({self._data})'


class ConsumeFloat(Provider):
    def __repr__(self):
        return f'ConsumeFloat({self._data})'


class ConsumeRegularFloat(Provider):
    def __repr__(self):
        return f'ConsumeRegularFloat()'


class ConsumeProbability(Provider):
    def __repr__(self):
        return f'ConsumeProbability()'


class ConsumeFloatInRange(Provider):
    def __repr__(self):
        return f'ConsumeFloatInRange({self._data})'


class ConsumeFloatList(Provider):
    def __repr__(self):
        return f'ConsumeFloatList({self._data})'


class ConsumeRegularFloatList(Provider):
    def __repr__(self):
        return f'ConsumeRegularFloatList({self._data})'


class ConsumeProbabilityList(Provider):
    def __repr__(self):
        return f'ConsumeProbabilityList({self._data})'


class ConsumeFloatListInRange(Provider):
    def __repr__(self):
        return f'ConsumeFloatListInRange({self._data})'


class PickValueInList(Provider):
    def __repr__(self):
        return f'PickValueInList({self._data})'


class ConsumeBool(Provider):
    def __repr__(self):
        return f'ConsumeBool()'
