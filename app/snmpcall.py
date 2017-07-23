from pysnmp.entity.rfc3413.oneliner import cmdgen
class snmpcall():
    def interfaces(self):
        cmdGen = cmdgen.CommandGenerator()

        errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.nextCmd(cmdgen.CommunityData('mpls_rw'),
                                            cmdgen.UdpTransportTarget(('192.168.10.110', 161)),
                                            '1.3.6.1.2.1.2.2.1.2', lookupNames=True, lookupValues=True
            )

        if errorIndication:
            print(errorIndication)
            self.interfaces=[str(errorIndication)]
            return self.interfaces
        else:
            if errorStatus:
                print('%s at %s' % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
                    )
                )
            else:
                self.interfaces = []
                for varBindTableRow in varBindTable:

                    for name, val in varBindTableRow:
                        # print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))
                        # print('%s' % val.prettyPrint())
                        if not val.prettyPrint()=='Null0':
                            self.interfaces.append('%s' % val.prettyPrint())

        
        return self.interfaces


