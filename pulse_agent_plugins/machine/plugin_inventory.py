# -*- coding: utf-8 -*-
from  lib.utils import pulginprocess
import sys, os
from  lib.utils import file_get_content, file_put_content, typelinux, servicelinuxinit, isprogramme, simplecommand, simplecommandstr, CreateWinUser
import zlib, base64
import traceback


plugin={"VERSION": "1.0", "NAME" :"inventory", "TYPE":"machine"}


@pulginprocess
def action( objetxmpp, action, sessionid, data, message, dataerreur, result):
    print "plugin_inventory"
    #result['base64'] = True
    if sys.platform.startswith('linux'):
        #obj = simplecommand("fusioninventory-agent  --stdout")
        try:
            obj = simplecommand("fusioninventory-agent  --stdout > /tmp/inventaire.txt")
            Fichier = open("/tmp/inventaire.txt",'r')
            result['data']['inventory'] = Fichier.read()
            Fichier.close()
            result['data']['inventory'] = base64.b64encode(zlib.compress(result['data']['inventory'],9))
        except Exception, e:
            print "Error: %s" % str(e)
            traceback.print_exc(file=sys.stdout)
            raise
    elif sys.platform.startswith('win'):
        try:
            program = os.path.join(os.environ["ProgramFiles"],'FusionInventory-Agent','fusioninventory-agent.bat')
            namefile = os.path.join(os.environ["ProgramFiles"], 'Pulse', 'tmp', 'inventaire.txt')
            cmd = """\"%s\" --local=\"%s\""""%(program,namefile)
            obj = simplecommand(cmd)
            Fichier = open(namefile,'r')
            result['data']['inventory'] = base64.b64encode(zlib.compress(Fichier.read(), 9))
            Fichier.close()
        except Exception, e:
            print "Error: %s" % str(e)
            traceback.print_exc(file=sys.stdout)
            raise
    elif sys.platform.startswith('darwin'):
        pass
