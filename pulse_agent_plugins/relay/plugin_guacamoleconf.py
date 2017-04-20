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

import sys
from  lib.utils import pluginprocess
import MySQLdb
import traceback
plugin = {"VERSION": "1.1", "NAME" :"guacamoleconf", "TYPE":"relayserver"}

def insertprotocole(protocole, hostname):
    return """INSERT INTO guacamole_connection (connection_name, protocol) VALUES ( '%s_%s', '%s');"""%(protocole.upper(), hostname, protocole.lower())

def deleteprotocole(protocole, hostname):
    return """DELETE FROM `guacamole_connection` WHERE connection_name = '%s_%s';"""%(protocole.upper(), hostname)

def insertparameter(index, parameter, value):
    return """INSERT INTO guacamole_connection_parameter (connection_id, parameter_name, parameter_value) VALUES (%s, '%s', '%s');"""%(index, parameter, value)

@pluginprocess
def action(objetxmpp, action, sessionid, data, message, dataerreur, result):
    try:
        db = MySQLdb.connect(host=objetxmpp.config.guacamole_dbhost,
                             user=objetxmpp.config.guacamole_dbuser,
                             passwd=objetxmpp.config.guacamole_dbpasswd,
                             db=objetxmpp.config.guacamole_dbname)
    except Exception as e:
        dataerreur['data']['msg'] = "MySQL Error: %s" % str(e)
        traceback.print_exc(file=sys.stdout)
        raise
    cursor = db.cursor()
    result['data']['uuid'] = data['uuid']
    result['data']['connection'] = {}

    if hasattr(objetxmpp.config, 'guacamole_protocols'):
        protos = objetxmpp.config.guacamole_protocols.split()
    else:
        protos = ['rdp', 'ssh', 'vnc']

    try:
        #delete connection
        for proto in protos:
            cursor.execute(deleteprotocole(proto, data['hostname']))
            db.commit()
        #create connection
        for proto in protos:
            result['data']['connection'][proto.upper()] = -1
            cursor.execute(insertprotocole(proto, data['hostname']))
            db.commit()
            result['data']['connection'][proto.upper()] = cursor.lastrowid
    except MySQLdb.Error, e:
        db.close()
        dataerreur['data']['msg'] = "MySQL Error: %s" % str(e)
        traceback.print_exc(file=sys.stdout)
        raise
    except Exception, e:
        dataerreur['data']['msg'] = "MySQL Error: %s" % str(e)
        traceback.print_exc(file=sys.stdout)
        db.close()
        raise
    ###################################
    ##configure parameters
    ###################################
    try:
        for proto in protos:
            if proto == 'rdp':
                port = '3389'
            elif proto == 'ssh':
                port = '22'
            else:
                port = '5901'
            cursor.execute(insertparameter(result['data']['connection'][proto.upper()], 'hostname', data['machine_ip']))
            db.commit()
            cursor.execute(insertparameter(result['data']['connection'][proto.upper()], 'port', port))
            db.commit()
            cursor.execute(insertparameter(result['data']['connection'][proto.upper()], 'color-depth', '24'))
            db.commit()
    except MySQLdb.Error, e:
        db.close()
        dataerreur['data']['msg'] = "MySQL Error: %s" % str(e)
        traceback.print_exc(file=sys.stdout)
        raise
    except Exception, e:
        dataerreur['data']['msg'] = "MySQL Error: %s" % str(e)
        traceback.print_exc(file=sys.stdout)
        db.close()
        raise
    db.close()