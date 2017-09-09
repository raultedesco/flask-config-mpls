from netmiko import ConnectHandler
from connect_device import ConnectDevice


class SendCommands(ConnectDevice):
    separated = '\n-----Verificacion de configuracion impactada-----\n'

    def save_config(self):
        get_running_config = 'show running-config'
        # Establecer Modo Ena
        self.net_connect.enable()


        print(self.net_connect.find_prompt())
        executed_running_config = self.net_connect.send_command(get_running_config)

        return executed_running_config

    def static_route(self, ip_destino, mascara, next_hop):
        # c = Commands()
        # static_route = c.getXmlCommand('static-route')
        space = ' '
        estatica = 'ip route'
        # Establecer Modo Ena
        self.net_connect.enable()

        # Armar Comando
        command = estatica + space + ip_destino + space + mascara + space + next_hop
        config_commands = [command]
        print(config_commands)
        print(self.net_connect.find_prompt())

        # Leer Current Config para  tener rollback del comando
        # current_config = self.net_connect.send_command('sh running-config')

        print(self.net_connect.find_prompt())
        executed_static_route = self.net_connect.send_config_set(config_commands)
        print(executed_static_route)
        print(self.net_connect.find_prompt())
        check = self.net_connect.send_command('show running-config partition ip-static-routes')
        # separated='\n-----Verificacion de configuracion impactada-----\n'
        executed_static_route += self.separated
        executed_static_route += check
        # Pasar Config a Lista para poder ejecutar send_config_set
        # content=[current_config]
        # print(content)
        # executed_current_config = self.net_connect.send_config_set(content)
        running_config  = self.save_config()

        return executed_static_route, running_config 

    def bgp(self, bgp_process=None, neighbor_ip=None, remote_as=None, network_ip=None):
        # c = Commands()
        # static_route = c.getXmlCommand('static-route')
        space = ' '
        bgp = 'router bgp'
        bgp_network = 'network'
        bgp_neighbor = 'neighbor'
        bgp_remote_as = 'remote-as'
        # Establecer Modo Ena
        self.net_connect.enable()

        # Armar Comando
        command_bgp = bgp + space + bgp_process
        command_bgp_network = bgp_network + space + network_ip
        command_bgp_neighbor = bgp_neighbor + space + neighbor_ip + space + bgp_remote_as + space + remote_as
        # command_bgp_end='end'

        config_commands_bgp = [command_bgp]
        config_commands_bgp.append(command_bgp_neighbor)
        config_commands_bgp.append(command_bgp_network)
        # config_commands_bgp.append(command_bgp_end)
        # config_commands_bgp.append(command_bgp_check_impact)

        # Leer Current Config para  tener rollback del comando
        # current_config = self.net_connect.send_command('sh running-config')

        print(self.net_connect.find_prompt())
        executed_bgp = self.net_connect.send_config_set(config_commands_bgp)
        # print(executed_bgp)

        print(self.net_connect.find_prompt())
        comando_verificacion_bgp = 'show running-config partition router bgp ' + bgp_process
        # print(comando_verificacion_bgp)
        check_bgp = self.net_connect.send_command(comando_verificacion_bgp)
        print(check_bgp)
        executed_bgp += self.separated
        executed_bgp += check_bgp

        # Pasar Config a Lista para poder ejecutar send_config_set
        # content=[current_config]
        # print(content)
        # executed_current_config = self.net_connect.send_config_set(content)

        return executed_bgp

    def interfaces(self, interface_value, ipaddress_value, mascara_value, state_value=None):
        space = ' '
        interface = 'interface'
        interface_value = interface_value
        ipaddress = 'ip address'
        ipaddress_value = ipaddress_value
        mascara_value = mascara_value
        if not state_value == None:
            self.state_value = state_value
        else:
            self.state_value = 'Down'
        self.net_connect.enable()
        command_interface = interface + space + interface_value
        command_set_interface = ipaddress + space + ipaddress_value + space + mascara_value
        if self.state_value == 'Up':
            command_state = 'no shutdown'
        else:
            command_state = 'shutdown'

        config_commands_interface = [command_interface]
        config_commands_interface.append(command_set_interface)
        config_commands_interface.append(command_state)

        print(self.net_connect.find_prompt())
        executed_interface = self.net_connect.send_config_set(config_commands_interface)
        print(executed_interface)
        print(self.net_connect.find_prompt())
        comando_verificacion_interfaces =\
            'show running-config partition interface ' + interface_value
        print(comando_verificacion_interfaces)
        check = self.net_connect.send_command(comando_verificacion_interfaces)
        executed_interface += self.separated
        executed_interface += check

        return executed_interface

    def interfaces_vrf(self, interface_value=None, interface_vrf_value=None, ipaddress_value=None, mascara_value=None, state_value=None):
        space = ' '
        interface_ip_vrf_forwarding = 'ip vrf forwarding'
        interface = 'interface'
        interface_value = interface_value
        ipaddress = 'ip address'
        ipaddress_value = ipaddress_value
        mascara_value = mascara_value
        if not state_value == None:
            self.state_value = state_value
        else:
            self.state_value = 'Down'
        self.net_connect.enable()
        command_interface = interface + space + interface_value
        command_set_vrf_forwarding_interface = interface_ip_vrf_forwarding + space + interface_vrf_value
        command_set_interface = ipaddress + space + ipaddress_value + space + mascara_value
        if self.state_value == 'Up':
            command_state = 'no shutdown'
        else:
            command_state = 'shutdown'

        config_commands_interface = [command_interface]
        config_commands_interface.append(command_set_vrf_forwarding_interface)
        config_commands_interface.append(command_set_interface)
        config_commands_interface.append(command_state)

        print(self.net_connect.find_prompt())
        executed_interface = self.net_connect.send_config_set(config_commands_interface)
        print(executed_interface)
        print(self.net_connect.find_prompt())
        comando_verificacion_interfaces =\
            'show running-config partition interface ' + interface_value
        print(comando_verificacion_interfaces)
        check = self.net_connect.send_command(comando_verificacion_interfaces)

        executed_interface += self.separated
        executed_interface += check

        return executed_interface

    def interfaces_mpls_ip(self, interface_value=None, ipaddress_value=None, mascara_value=None, state_value=None):
        space = ' '
        interfaces_mpls_ip = 'mpls ip'
        interface = 'interface'
        interface_value = interface_value
        ipaddress = 'ip address'
        ipaddress_value = ipaddress_value
        mascara_value = mascara_value
        if not state_value == None:
            self.state_value = state_value
        else:
            self.state_value = 'Down'
        self.net_connect.enable()
        command_interface = interface + space + interface_value
        command_set_interface = ipaddress + space + ipaddress_value + space + mascara_value
        command_set_mpls_ip = interfaces_mpls_ip
        if self.state_value == 'Up':
            command_state = 'no shutdown'
        else:
            command_state = 'shutdown'

        config_commands_interface = [command_interface]
        config_commands_interface.append(command_set_interface)
        config_commands_interface.append(command_set_mpls_ip)
        config_commands_interface.append(command_state)

        print(self.net_connect.find_prompt())
        executed_interface = self.net_connect.send_config_set(config_commands_interface)
        print(executed_interface)
        print(self.net_connect.find_prompt())
        comando_verificacion_interfaces =\
            'show running-config partition interface ' + interface_value
        print(comando_verificacion_interfaces)
        check = self.net_connect.send_command(comando_verificacion_interfaces)

        executed_interface += self.separated
        executed_interface += check

        return executed_interface

    def eigrp(self, eigrp_process=None,
              eigrp_network_IP=None, eigrp_wildcard=None):
        # c = Commands()
        # static_route = c.getXmlCommand('static-route')
        space = ' '
        eigrp = 'router eigrp'
        eigrp_network = 'network'

        # Establecer Modo Ena
        self.net_connect.enable()

        # Armar Comando
        command_eigrp = eigrp + space + eigrp_process
        command_eigrp_network = eigrp_network + space + eigrp_network_IP + space + eigrp_wildcard
        # command_bgp_end='end'
        # command_bgp_check_impact='show running-config partition router 100'

        config_commands_eigrp = [command_eigrp]

        # config_commands_bgp_neighbor = [command_bgp_neighbor]
        # config_commands_bgp_remote_as = [command_bgp_network]
        config_commands_eigrp.append(command_eigrp_network)

        # config_commands_bgp.append(command_bgp_end)
        # config_commands_bgp.append(command_bgp_check_impact)

        # Leer Current Config para  tener rollback del comando
        # current_config = self.net_connect.send_command('sh running-config')

        print(self.net_connect.find_prompt())
        executed_eigrp = self.net_connect.send_config_set(config_commands_eigrp)
        # print(executed_bgp)

        print(self.net_connect.find_prompt())
        comando_verificacion_eigrp = 'show running-config partition router eigrp ' + eigrp_process
        # print(comando_verificacion_bgp)
        check_eigrp = self.net_connect.send_command(comando_verificacion_eigrp)
        print(check_eigrp)
        executed_eigrp += self.separated
        executed_eigrp += check_eigrp

        # Pasar Config a Lista para poder ejecutar send_config_set
        # content=[current_config]
        # print(content)
        # executed_current_config = self.net_connect.send_config_set(content)

        return executed_eigrp

    def ospf(self, ospf_process=None, ospf_network_value=None, ospf_area_value=None):
        space = ' '
        ospf = 'router ospf'
        ospf_network = 'network'
        ospf_area = 'area'

        # Establecer Modo Ena
        self.net_connect.enable()

        # Armar Comando
        command_ospf = ospf + space + ospf_process
        command_ospf_network = ospf_network + space + \
            ospf_network_value + space + ospf_area + space + ospf_area_value

        # agregar Comando a Lista a pasar a ejecucion
        config_commands_ospf = [command_ospf]

        config_commands_ospf.append(command_ospf_network)

        print(self.net_connect.find_prompt())
        executed_ospf = self.net_connect.send_config_set(config_commands_ospf)
        # print(executed_bgp)

        print(self.net_connect.find_prompt())
        comando_verificacion_ospf = 'show running-config partition router ospf ' + ospf_process
        # print(comando_verificacion_bgp)
        check_ospf = self.net_connect.send_command(comando_verificacion_ospf)
        print(check_ospf)
        executed_ospf += self.separated
        executed_ospf += check_ospf

        return executed_ospf

    def iBGP_mpls(self, bgp_process_value=None, remote_as_internal=None, bgp_neighbor_internal_value=None):
        space = ' '
        bgp = 'router bgp'
        bgp_network = 'network'
        bgp_neighbor = 'neighbor'
        bgp_remote_as = 'remote-as'
        bgp_neighbor_activate = 'activate'

        # Establecer Modo Ena
        self.net_connect.enable()

        cmd_bgp = bgp + space + bgp_process_value
        cmd_neighbor = bgp_neighbor + space + bgp_neighbor_internal_value\
            + space + bgp_remote_as + space + remote_as_internal

        config_commands_ibgp_mpls = [cmd_bgp]
        config_commands_ibgp_mpls.append(cmd_neighbor)

        print(self.net_connect.find_prompt())
        executed_ibgp_mpls =\
            self.net_connect.send_config_set(config_commands_ibgp_mpls)

        print(self.net_connect.find_prompt())
        cmd_verificacion_ibgp_mpls = 'show running-config partition router bgp ' + bgp_process_value

        check_ibgp_mpls = \
            self.net_connect.send_command(cmd_verificacion_ibgp_mpls)
        print(check_ibgp_mpls)
        executed_ibgp_mpls += self.separated
        executed_ibgp_mpls += check_ibgp_mpls

        return executed_ibgp_mpls

    def iBGP_extended_community(self, bgp_process_value=None, bgp_neighbor_internal_value=None):
        space = ' '
        bgp = 'router bgp'
        bgp_network = 'network'
        bgp_neighbor = 'neighbor'
        bgp_remote_as = 'remote-as'
        bgp_neighbor_activate = 'activate'
        bgp_address_family = 'address-family ipv4 vrf'
        bgp_vpnv4_family = ' address-family vpnv4'
        bgp_vpnv4_community = 'send-community extended'

        # Establecer Modo Ena
        self.net_connect.enable()

        # Armar Comando
        cmd_bgp = bgp + space + bgp_process_value
        cmd_bgp_vpnv4_family = bgp_vpnv4_family
        cmd_neighbor_activate = bgp_neighbor + space + \
            bgp_neighbor_internal_value + space + bgp_neighbor_activate
        cmd_send_community = bgp_neighbor + space + bgp_neighbor_internal_value\
            + space + bgp_vpnv4_community

        print(cmd_bgp)
        print(cmd_bgp_vpnv4_family)
        print(cmd_neighbor_activate)
        print(cmd_send_community)

        config_commands_ibgp_ec = [cmd_bgp]
        config_commands_ibgp_ec.append(cmd_bgp_vpnv4_family)
        config_commands_ibgp_ec.append(cmd_neighbor_activate)
        config_commands_ibgp_ec.append(cmd_send_community)

        print(self.net_connect.find_prompt())
        executed_ibgp_ec =\
            self.net_connect.send_config_set(config_commands_ibgp_ec)

        print(self.net_connect.find_prompt())
        cmd_verificacion_ibgp_ec = 'show running-config partition router bgp ' + bgp_process_value

        check_ibgp_ec = \
            self.net_connect.send_command(cmd_verificacion_ibgp_ec)
        print(check_ibgp_ec)
        executed_ibgp_ec += self.separated
        executed_ibgp_ec += check_ibgp_ec
        return executed_ibgp_ec

    def eBGP_vrf(self, bgp_process_value=None, ebgp_remote_as=None,  bgp_neighbor_external_value=None, vrf_value=None):
        space = ' '
        bgp = 'router bgp'
        bgp_network = 'network'
        bgp_neighbor = 'neighbor'
        bgp_remote_as = 'remote-as'
        bgp_neighbor_activate = 'activate'
        bgp_address_family = 'address-family ipv4 vrf'
        bgp_address_family_rc = 'redistribute connected'

        # Establecer Modo Ena
        self.net_connect.enable()

        # Armar Comando
        cmd_bgp = bgp + space + bgp_process_value
        cmd_address_family = bgp_address_family + space + vrf_value
        cmd_neighbor_vrf = bgp_neighbor + space +\
            bgp_neighbor_external_value + space + bgp_remote_as + space + ebgp_remote_as
        cmd_neighbor_activate = bgp_neighbor + \
            space + bgp_neighbor_external_value + space + bgp_neighbor_activate
        cmd_address_family_rc = bgp_address_family_rc

        print(cmd_bgp)
        print(cmd_address_family)
        print(cmd_neighbor_vrf)
        print(cmd_address_family_rc)

        config_commands_ebgp_vrf = [cmd_bgp]
        config_commands_ebgp_vrf.append(cmd_address_family)
        config_commands_ebgp_vrf.append(cmd_neighbor_vrf)
        config_commands_ebgp_vrf.append(cmd_neighbor_activate)
        config_commands_ebgp_vrf.append(cmd_address_family_rc)

        print(self.net_connect.find_prompt())
        executed_ebgp_vrf =\
            self.net_connect.send_config_set(config_commands_ebgp_vrf)

        print(self.net_connect.find_prompt())
        cmd_verificacion_ebgp_vrf = 'show running-config partition router bgp ' + bgp_process_value
        check_ebgp_vrf = \
            self.net_connect.send_command(cmd_verificacion_ebgp_vrf)
        print(check_ebgp_vrf)
        executed_ebgp_vrf += self.separated
        executed_ebgp_vrf += check_ebgp_vrf

        return executed_ebgp_vrf

    def vrf(self, vrf_name=None, vrf_rd_value=None, vrf_rt_value=None):
        space = ' '
        vrf = 'ip vrf'
        vrf_rd = 'rd'
        vrf_rt = 'route-target'

        # Establecer Modo Ena
        self.net_connect.enable()

        # Armar Comando
        command_vrf = vrf + space + vrf_name
        command_vrf_rd = vrf_rd + space + vrf_rd_value
        command_vrf_rt = vrf_rt + space + vrf_rt_value

        config_commands_vrf = [command_vrf]
        config_commands_vrf.append(command_vrf_rd)
        config_commands_vrf.append(command_vrf_rt)

        print(self.net_connect.find_prompt())
        executed_vrf = self.net_connect.send_config_set(config_commands_vrf)
        # print(executed_bgp)

        print(self.net_connect.find_prompt())
        comando_verificacion_vrf = 'show running-config vrf ' + vrf_name
        # print(comando_verificacion_bgp)
        check_vrf = self.net_connect.send_command(comando_verificacion_vrf)
        print(check_vrf)
        executed_vrf += self.separated
        executed_vrf += check_vrf

        return executed_vrf

    def ip_brief_and_routes(self):
        # Establecer Modo Ena
        self.net_connect.enable()

        # Armar Comando
        show_ip_interface_brief = 'show ip interface brief'
        show_ip_route = 'show ip route'
        # Ejecutar Comando
        check_ip_brief = self.net_connect.send_command(show_ip_interface_brief)

        check_ip_route = self.net_connect.send_command(show_ip_route)

        return check_ip_brief, check_ip_route
