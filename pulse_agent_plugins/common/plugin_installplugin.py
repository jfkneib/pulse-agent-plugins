# -*- coding: utf-8 -*-
#
# (c) 2016 siveo, http://www.siveo.net
#
# This file is part of Pulse 2, http://www.siveo.net
#
# Pulse 2 is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Pulse 2 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pulse 2; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.
import os
import logging


plugin={"VERSION": "1.1", "NAME" : "installplugin", "TYPE" : "all"}

def action( objetxmpp, action, sessionid, data, message, dataerreur ):
    if action == 'installplugin':
        if len(data) != 0 :
            namefile =  os.path.join(objetxmpp.config.pathplugins, data['pluginname'])

            try:
                fileplugin = open(namefile, "w")
                fileplugin.write(str(data['datafile']))
                fileplugin.close()
            except Exception, e:
                logging.getLogger().debug("error : %s"%str(e))
                return
            msg = "install plugin %s on %s"%(data['pluginname'],message['to'].user)
            objetxmpp.loginfotomaster(msg)
