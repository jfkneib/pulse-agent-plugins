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

import logging

plugin = {"VERSION" : "1.0", "NAME" : "enddeploy",  "TYPE" : "all"}


def action( objectxmpp, action, sessionid, data, message, dataerreur):
    logging.getLogger().debug("###################################################")
    logging.getLogger().debug("call %s from %s"%(plugin,message['from']))
    logging.getLogger().debug("###################################################")

    objectxmpp.ban_deploy_sessionid_list.append(sessionid)
    # in 900 secondes on call  remove_sessionid_in_ban_deploy_sessionid_list function
    objectxmpp.schedule('removeban',
                        objectxmpp.lapstimebansessionid,
                        objectxmpp.remove_sessionid_in_ban_deploy_sessionid_list,
                        args=(sessionid,),
                        repeat=False)
