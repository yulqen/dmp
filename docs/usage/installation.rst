Installation
============

``dmp`` is not available on `PyPi <https://pypi.org>`_ - you must install from the private repository on Github at `https://github.com/yulqen/dmp <https://github.com/yulqen/dmp>`_.

.. py:function:: spam(eggs)

   This function takes a bunch of eggs and spams them across the boundaries.

.. py:data:: SLOTH
   :type: string
   :value: PUNGATIONS

.. py:class:: AbstractRepository

    .. py:method:: add()
      :abstractmethod:

      Add an item.

    .. py:method:: get()
      :abstractmethod:

      Get an item.

    .. py:method:: list()
      :abstractmethod:

      List items.

.. note::
   This is a note that you must take note of!

.. warning::
   This is a warning and we must obey (or at least take responsibility when we stray).

.. seealso::

   Module :py:mod:`zipfile`
      Documentation of the :py:mod:`zipfile` standard module.

 .. code-block:: python
   :caption: Print an expression multiple times 
   
   print('This is smashing')
   for x in range(200):
      print("Clunch")


Chubby
------
.. hlist::
   :columns: 2

   * This is ace.
   * Web sites are a good idea.
   * I don't know if this looks good.
   * Sphinx and reStructured text are for pros - markdown is for sissies!
   * There is a vote of confidence in Brosman Johnson this evening
   * A blackbird is the representative of gloom but also joy.

Very briefly, these are instructions for setting up the development environment::

   git clone git@github.com:yulqen/dmp.git
   cd dmp
   python -m venv .venv
   . .venv/bin/activate
   pip install -e .
   pip install -r requirements_dev.txt

The python packages are contained within a ``src`` directory which allows for installing locally in develop mode (using ``pip install -e .``) and for the ``tests`` directory to remain outside of the build package.
