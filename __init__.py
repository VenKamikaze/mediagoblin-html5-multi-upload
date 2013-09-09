# GNU MediaGoblin -- federated, autonomous media hosting
# Copyright (C) 2011, 2012 MediaGoblin contributors.  See AUTHORS.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# Created by Mick Saunders


import logging
import os

from mediagoblin.tools import pluginapi

PLUGIN_DIR = os.path.dirname(__file__)

_log = logging.getLogger(__name__)

def setup_plugin():
    config = pluginapi.get_config('mediagoblin.plugins.html5-multi-upload')

    _log.info('Setting up html5-multi-upload....')

    # Register the template path.
    pluginapi.register_template_path(os.path.join(PLUGIN_DIR, 'templates'))

    pages = config.items()

    routes = [
         ('mediagoblin.plugins.html5-multi-upload.multi_submit_start',
          '/html5-multi-upload/', 
          'mediagoblin.plugins.html5-multi-upload.views:multi_submit_start')
      ]

    pluginapi.register_routes(routes)
    _log.info('Done setting up html5-multi-upload!')


hooks = {
    'setup': setup_plugin
    }
