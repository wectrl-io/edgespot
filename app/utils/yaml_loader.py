#!/usr/bin/env python3
# -*- coding: utf8 -*-

import os
import yaml

class Loader(yaml.SafeLoader):
    """Custum YAML loader.
    """

#region Constructor

    def __init__(self, stream):
        """Construcotr

        Args:
            stream (stream): Fle stream.
        """

        self._root = os.path.split(stream.name)[0]

        super(Loader, self).__init__(stream)

#endregion

#region Public Methods

    def include(self, node):
        """Include file from name in file.

        Args:
            node (_type_): Inside file node.

        Returns:
            _type_: _description_
        """

        filename = os.path.join(self._root, self.construct_scalar(node))

        with open(filename, 'rt') as stream:
            return yaml.load(stream, Loader)

#endregion

# Add include flag (command)
Loader.add_constructor('!include', Loader.include)
