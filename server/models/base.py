class Base:
    '''
    A base class that inherits all keyword arguments and stores them as unknown params
    '''
    def __init__(self, **kwargs) -> None:
        self.__unknown_params = kwargs

