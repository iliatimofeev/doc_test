class DocTestClass(object):
    """TopLevelLayerSpec schema wrapper

    Mapping(required=[layer])

    Attributes
    ----------
    layer : List(anyOf(LayerSpec, CompositeUnitSpec))
        Layer or single view specifications to be layered.

        **Note** : Specifications inside ``layer`` cannot use ``row`` and ``column`` channels as layering facet specifications is not allowed.
     
    transform : List(Transform)
        An array of data transformations such as filter and new field calculation.
        width : float
        The width of a visualization.

        **Default value:** This will be determined by the
        following rules:

        * If a view's `autosize <https://vega.github.io/vega-
          lite/docs/size.html#autosize>`_ type is ``"fit"`` or
          its x-channel has a `continuous scale
          <https://vega.github.io/vega-lite/
          docs/scale.html#
          continuous>`_,
          the width will be the value of `config.view.width
          <https://vega.github.io/vega-lite/docs/spec.html#config>`_.
        * For x-axis with a band or point scale: if `rangeStep <https://vega.github.io/vega-lite/docs/scale.html#band>`_ is a numeric value or unspecified, the width is `determined by the range step, paddings, and the cardinality of the field mapped to x-channel <https://vega.github.io/vega-lite/docs/scale.html#band>`_.   Otherwise, if the ``rangeStep`` is ``null``, the width will be the value of `config.view.width <https://vega.github.io/vega-lite/docs/spec.html#config>`_. 
        * If no field is mapped to ``x`` channel, the ``width`` will be the value of `config.scale.textXRangeStep <https://vega.github.io/vega-lite/docs/size.html#default-width-and-height>`_ for ``text`` mark and the value of ``rangeStep`` for other marks.  

        **Note:** For plots with 
        `row and column channels 
        <https://vega.github.io/vega-lite/
        docs/encoding.html#facet>`_,
        this represents the width of a single view.

        **See also:** The documentation for `width and height
        <https://vega.github.io/vega-lite/docs/size.html>`_ contains more examples.

    """
    def method(self):
        """Short derscd"""
        return True


class ExampleTableUse(object):
    """.. altair-object-table:: altair.LayerChart

    """
    pass


class ExampleClass(object):
    """The summary line for a class docstring should fit on one line.

    If the class has public attributes, they may be documented here
    in an ``Attributes`` section and follow the same formatting as a
    function's ``Args`` section. Alternatively, attributes may be documented
    inline with the attribute's declaration (see __init__ method below).

    Properties created with the ``@property`` decorator should be documented
    in the property's getter method.

    Attributes
    ----------
    attr1 : str
        Description of `attr1`.
    attr2 : :obj:`int`, optional
        Description of `attr2`.

    """

    def __init__(self, param1, param2, param3):
        """Example of docstring on the __init__ method.

        The __init__ method may be documented in either the class level
        docstring, or as a docstring on the __init__ method itself.

        Either form is acceptable, but the two should not be mixed. Choose one
        convention to document the __init__ method and be consistent with it.

        Note
        ----
        Do not include the `self` parameter in the ``Parameters`` section.

        Parameters
        ----------
        param1 : str
            Description of `param1`.
        param2 : :obj:`list` of :obj:`str`
            Description of `param2`. Multiple
            lines are supported.
        param3 : :obj:`int`, optional
            Description of `param3`.

        """
        self.attr1 = param1
        self.attr2 = param2
        self.attr3 = param3  #: Doc comment *inline* with attribute

        #: list of str: Doc comment *before* attribute, with type specified
        self.attr4 = ["attr4"]

        self.attr5 = None
        """str: Docstring *after* attribute, with type specified."""

    @property
    def readonly_property(self):
        """str: Properties should be documented in their getter method."""
        return "readonly_property"

    @property
    def readwrite_property(self):
        """:obj:`list` of :obj:`str`: Properties with both a getter and setter
        should only be documented in their getter method.

        If the setter method contains notable behavior, it should be
        mentioned here.
        """
        return ["readwrite_property"]

    @readwrite_property.setter
    def readwrite_property(self, value):
        value

    def example_method(self, param1, param2):
        """Class methods are similar to regular functions.

        Note
        ----
        Do not include the `self` parameter in the ``Parameters`` section.

        Parameters
        ----------
        param1
            The first parameter.
        param2
            The second parameter.

        Returns
        -------
        bool
            True if successful, False otherwise.

        """
        return True

    def __special__(self):
        """By default special members with docstrings are not included.

        Special members are any methods or attributes that start with and
        end with a double underscore. Any special member with a docstring
        will be included in the output, if
        ``napoleon_include_special_with_doc`` is set to True.

        This behavior can be enabled by changing the following setting in
        Sphinx's conf.py::

            napoleon_include_special_with_doc = True

        """
        pass

    def __special_without_docstring__(self):
        pass

    def _private(self):
        """By default private members are not included.

        Private members are any methods or attributes that start with an
        underscore and are *not* special. By default they are not included
        in the output.

        This behavior can be changed such that private members *are* included
        by changing the following setting in Sphinx's conf.py::

            napoleon_include_private_with_doc = True

        """
        pass

    def _private_without_docstring(self):
        pass
