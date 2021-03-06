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
# file : pulse_agent_plugins/relay/plugin_cluster.py
import json
import logging
logger = logging.getLogger()

DEBUGPULSEPLUGIN = 25

plugin = { "VERSION" : "1.0006", "NAME" : "cluster", "TYPE" : "relayserver", "DESC" : "update list ARS cluster" }

def refreshremotears(objectxmpp, action, sessionid):
    for ars in objectxmpp.jidclusterlistrelayservers:
        result = {
                        'action': "%s"%action,
                        'sessionid': sessionid,
                        'data' :  { "subaction" : "refreshload", 
                                    "data" : { "chargenumber" : objectxmpp.checklevelcharge() 
                                    } 
                        },
                        'ret' : 0,
                        'base64' : False
        }
        objectxmpp.send_message( mto=ars,
                        mbody=json.dumps(result),
                        mtype='chat')
    logging.getLogger().debug("plugin cluster : refresh charge (%s) of ars %s to list remote ars cluster %s"%\
                                                    ( objectxmpp.checklevelcharge(),\
                                                    objectxmpp.boundjid.bare,\
                                                    objectxmpp.jidclusterlistrelayservers))


def action( objectxmpp, action, sessionid, data, message, dataerreur):
    logging.getLogger().debug("call %s from %s"%(plugin,message['from']))
    print json.dumps(data, indent = 4)
    if "subaction" in data:
        if data['subaction'] == "initclusterlist":
            # update list cluster jid
            #list friend ars
            jidclusterlistrelayservers = [jidrelayserver for jidrelayserver in data['data'] if jidrelayserver != message['to']]

            # delete reference ARS si pas dans jidclusterlistrelayservers
            for ars in jidclusterlistrelayservers:
                if not ars in objectxmpp.jidclusterlistrelayservers:
                    objectxmpp.jidclusterlistrelayservers[ars] = { 'chargenumber' : 0 }

            delars=[]
            for ars in objectxmpp.jidclusterlistrelayservers:
                if not ars in jidclusterlistrelayservers:
                    delars.append(ars)

            for ars in delars:
                del objectxmpp.jidclusterlistrelayservers[ars]

            for ars in objectxmpp.jidclusterlistrelayservers:
                result = {
                                'action': "%s"%action,
                                'sessionid': sessionid,
                                'data' :  { "subaction" : "refreshload", 
                                            "data" : { "chargenumber" : objectxmpp.levelcharge } },
                                'ret' : 0,
                                'base64' : False
                    }
                print ars
                print result
                objectxmpp.send_message( mto=ars,
                                            mbody=json.dumps(result),
                                            mtype='chat')
            logging.getLogger().debug("new ARS list friend of cluster : %s"% objectxmpp.jidclusterlistrelayservers)
        elif data['subaction'] == "refreshload":
            objectxmpp.jidclusterlistrelayservers[message['from']] = data['data']
            logging.getLogger().debug("new ARS list friend of cluster : %s"% objectxmpp.jidclusterlistrelayservers)
        elif data['subaction'] == "removeresource":
            resource = objectxmpp.checklevelcharge(-1)
            refreshremotears(objectxmpp, action, sessionid)
            objectxmpp.xmpplog('plugin Cluster : charge ARS (%s): %s'%(objectxmpp.boundjid.bare, resource),
                                type = 'deploy',
                                sessionname = sessionid,
                                priority = -1,
                                action = "",
                                who = objectxmpp.boundjid.bare,
                                how = "",
                                why = "",
                                module = "Deployment | Cluster | Notify",
                                date = None ,
                                fromuser = data['data']['user'],
                                touser = "")
        elif data['subaction'] == "takeresource":
            resource = objectxmpp.checklevelcharge(1)
            refreshremotears(objectxmpp, action, sessionid)
            objectxmpp.xmpplog('plugin Cluster : charge ARS (%s): %s'%(objectxmpp.boundjid.bare, resource),
                                type = 'deploy',
                                sessionname = sessionid,
                                priority = -1,
                                action = "",
                                who = objectxmpp.boundjid.bare,
                                how = "",
                                why = "",
                                module = "Deployment | Cluster | Notify",
                                date = None ,
                                fromuser = data['data']['user'],
                                touser = "")
    #result = {
                #'action': "result%s"%action,
                #'sessionid': sessionid,
                #'data' : objectxmpp.jidclusterlistrelayservers,
                #'ret' : 0,
                #'base64' : False }


    ##message
    #objectxmpp.send_message( mto=message['from'],
                             #mbody=json.dumps(result),
                             #mtype='chat')
