Extend MQ², write your own plugin
=================================

If you the QTL mapping tool you use is not currently supported by MQ²,
it might be easily added by adding a plugin specific to this format/tool.

To create a new plugin, you will need to create a new python file, place
it under ``MQ2/plugins/``. This python file should contain its own class
which inherits and implements the method defined in ``PluginInterface``.


Plugin interface:
-----------------


.. autoclass:: MQ2.plugin_interface.PluginInterface
   :members:
