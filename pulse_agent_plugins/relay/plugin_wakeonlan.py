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

from  lib.utils import pluginprocess
from wakeonlan import wol

plugin={"VERSION": "1.1", "NAME" :"wakeonlan","TYPE":"relayserver"}
@pluginprocess
def action( objetxmpp, action, sessionid, data, message, dataerreur,result):
    print data
    try:
        wol.send_magic_packet(data['macaddress'])
        result['data']['start'] = "ok"
    except:
        dataerreur['data']['msg'] = "ERROR : plugin wakeonlan"
        dataerreur['ret'] = 255
        raise
