class DocstringClassExample:
    """
    Class that serves as an example of docstring documentation

    Attributes
    ----------
    attribute1 : str
        first parameter of a class, that is never used
    attribute2 : np.array
        second parameters that also is not used

    Methods
    -------
    example_method1(param)
        Only raises FileNotFoundError, so...
    example_method1(param=None)
        Also only raises FileNotFoundError, but more efficiently since param has a default value
    """

    def __init__(self, parameter1, parameter2):
        """
        Parameters
        ----------
        parameter1 : str
            Value of attribute1
        parameter2 : list
            Value of attribute2
        """
        self.attribute1 = parameter1
        self.attribute2 = parameter2

    def example_method1(self, param):
        """
        As was stated before, it just raises FileNotFoundError, no matter what You do

        Parameters
        ----------
        param : any
           Just a param that changes nothing

        Raises
        ------
        FileNotFoundError
           It is raised no matter what, a fate You cannot escape

        Returns
        -------
        """

        raise FileNotFoundError()

    def example_method2(self, param=None):
        """
        As was stated before, it just raises FileNotFoundError, no matter what You do, but is more effective at
        raising that exception since You don't need to specify param

        Parameters
        ----------
        param : any, optional
           Just a param that makes method raise Error no matter what will You do (default is None)

        Raises
        ------
        FileNotFoundError
           It is raised no matter what, a fate You cannot escape

        Returns
        -------
        """
        raise FileNotFoundError()