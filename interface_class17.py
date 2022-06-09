import paramiko
import time   

FCP_List = ["NEDAGOSTAR", "RIGHTEL", "ARYARESANE", "ARIARESANE", "ARYARESANEH",
            "SHATEL", "FARMANDARI", "ASIYATEC", "ASIATEC", "ASIATEK", "ASIATECH", "ASYIATEK", "HELMA", "PISHGAMAN",
            "DADEGOSTAR", "DADEHGOSTAR", "FARAGOSTAR", "FANAVA", "ERTEBATAT SABET PARSIAN", "QOS"]
int_types = ('ISIS_UpLink', 'IPOSS_Uplink', 'ShutDown', 'LoopBack', 'Vlan', 'NULL', 'vty', 'VlanIF')
VPN_types = {'xconnect ':               'Xconnect',
             'ip vrf forwarding ':      'IP-vrf-forwarding',
             'mpls l2vc ':              'MPLS-l2',
             'l2 binding vsi ':         'l2-VSI',
             'ip binding vpn-instance ':'vpn-instance' }
Encapsulation_types = {'encapsulation qinq vid':              'QinQ', 
                       'qinq termination pe-vid':             'QinQ',
                       'qinq stacking pe-vid':                'QinQ',
                       'qinq stacking vid':                   'QinQ',
                       'qinq vid':                            'QinQ',
                       'dot1q termination vid':               'Dot1q',
                       'vlan-type dot1q':                     'Dot1q',
                       'encapsulation dot1Q ':                'Dot1q',
                       'encapsulation dot1q ':                'Dot1q',
                       'encapsulation ppp':                   'PPP',  
                       'switchport trunk allowed vlan':       'Trunk',
                       'port trunk allow-pass ':              'Trunk',
                       'switchport access vlan':              'Access',
                       'port default access vlan':            'Access'}

class Interface():
    def __init__(self, config):
        self.config = config
        self.Type = "" 
        self.Valid = False
        self.Name = ""
        self.Description =""
        self.ID = "0"
        self.IP = ""
        self.Encap = list("",)
        self.Problem = False
        self.FCP = False
        self.Profile = ""
        self.DCRM_Profile = ""
        self.VPN = list("",)
        
        self._RunEachFunc([self.Set_Port(), self.Set_Des(), self.Set_ID(), self.Set_IP(), 
                          self.Set_VPN(), self.Set_Encapsulation(), self.FCP_exception()])
                
    #++++++++++++++++++++++++++++++++++++
    def _RunEachFunc(self, FuncList):
        result = []
        for i in range(len(FuncList)):
            result.append(FuncList[i])
        return result    

    #++++++++++++++++++++++++++++++++++++
    def _Find_Int_Param(self, start, end, characters = None):
        my_parameter = ""
        
        if characters is None:
            characters = self.config
            
        start_param = characters.find(start)
        end_param = characters.find(end, start_param +1)
        if start_param != -1 :
            my_parameter = characters[start_param + len(start) : end_param ] 
        return my_parameter
    #++++++++++++++++++++++++++++++++++++    
    def Set_Des(self):
        start = "description "
        end = "\n"
        self.Description = self._Find_Int_Param(start, end) 
    #++++++++++++++++++++++++++++++++++++
    def Set_Port(self):
        start = "interface "
        end = "\n"
        self.Name = self._Find_Int_Param(start, end) 
    #++++++++++++++++++++++++++++++++++++
    def Set_IP(self):
        start = "ip address "
        end = "\n"
        IP = self._Find_Int_Param(start, end) 
        if IP.split(".")[0].isnumeric():
            self.IP = IP
  
    #++++++++++++++++++++++++++++++++++++
    def Set_ID(self):
        my_desc = self.Description
        if my_desc != "":
            start = "\""
            end = "\""
            ID_str = self._Find_Int_Param(start, end, my_desc).strip()
            if ID_str.isnumeric():
                self.ID = ID_str
            else:
                self.ID = "0"
    #++++++++++++++++++++++++++++++++++++
    def Set_VPN(self):  
        for key, value in VPN_types.items():
            #print(key, '->', value)
            end = "\n"
            if self.config.find(key)!= -1:
                self.VPN.append(value + ' ')
                start = key
                if key == "xconnect ":
                    end = "encapsulation"  
                self.VPN.append(self._Find_Int_Param(start, end).strip())
                return      
    #++++++++++++++++++++++++++++++++++++
    def Set_Encapsulation(self):  
        for key, value in Encapsulation_types.items():
            #print(key, '->', value)
            end = "\n"
            if self.config.find(key)!= -1:
                self.Encap.append(value)
                start = key
                if (key == "qinq termination pe-vid") or (key == "encapsulation qinq vid"):
                    end = "ce-vid "  
                    self.Encap.append(self._Find_Int_Param(start, end).strip())
                    start = "ce-vid "
                    end = "\n"
                    self.Encap.append(self._Find_Int_Param(start, end).strip())
                    return
                self.Encap.append(self._Find_Int_Param(start, end).strip())
                return          
    #++++++++++++++++++++++++++++++++++++ 
    def Show_Config(self):
        return self.config
    #++++++++++++++++++++++++++++++++++++ 
    def Show_Interface(self, router_name):
        result = ( router_name, self.Name, self.Description, self.Encap, self.ID, self.IP, 
                  self.VPN, self.Profile, self.Type )
        return result
    #++++++++++++++++++++++++++++++++++++ 
    def Find_Description(self, int_Des, router_name):
        if self.Description.find(int_Des) != -1:
            return  self.Show_Interface(router_name)
        else:
            return False 
    #++++++++++++++++++++++++++++++++++++ 
    def Find_ID(self, int_ID, router_name): 
        if self.ID.find(int_ID) != -1:
            return self.Show_Interface(router_name)
        else:
            return False 
    #++++++++++++++++++++++++++++++++++++ 
    def Find_IP(self, int_IP, router_name):   
        if self.IP.find(int_IP) != -1:
             return self.Show_Interface(router_name)
        else:
            return False 
    #++++++++++++++++++++++++++++++++++++ 
    def Find_Port(self, int_name, router_name):   
        if self.Name.find(int_name) != -1:
            return self.Show_Interface(router_name)
        else:
            return False      
    #++++++++++++++++++++++++++++++++++++  
    def _Return_IP(self): 
        return self.IP  
              
    #++++++++++++++++++++++++++++++++++++ 
    def Find_Free_Ports(self, router):
        if self.IP == '':
            if self.Description == '' :
                if self.Type == "":
                    if self.Encap == []:
                        if self.VPN == []:
                            return self.Show_Interface(router)
        else:
            return False
        
    #++++++++++++++++++++++++++++++++++++
    def Find_IP_INET(self):
        '''Find Interface's IP in INET and not start with 10'''
        if self.IP != '':
            contain_INET = self.Show_Config().find('INET')
            IP_split = self.IP.split(".")
            first_ten= IP_split[0]
            
            if first_ten != '10':   
                if contain_INET != -1:
                    return self.IP
        else:
            return False
                 
    #++++++++++++++++++++++++++++++++++++
    def Find_H_profile(self):
        Port_qos = ""
    
        Por_location = self.config.find("qos-profile")
        ening = self.config.find("inbound", Por_location + 1) -1
        
        if Por_location != -1 :
            Port_qos = self.config[Por_location + len("qos-profile") +1: ening ]
        self.Profile = Port_qos
    #++++++++++++++++++++++++++++++++++++
    def Find_CR_profile(self):
        Port_qos = ""
      
        Por_location = self.config.find("service-policy input")
        ening = self.config.find("\n", Por_location +1 + len ("service-policy input"))
    
        if Por_location != -1 :
            Port_qos = self.config[Por_location + len("service-policy input") +1: ening ]
    
        self.Profile = Port_qos
    #++++++++++++++++++++++++++++++++++++
    def Find_CSW_profile(self):
        Port_qos = "" 
        #srr-queue bandwidth shape 250 250 250 250
    #++++++++++++++++++++++++++++++++++++
    def FCP_exception(self):
        each_names = self.config.split(" ")
        for j in each_names:
            for i in FCP_List:
                if i == j:
                    self.FCP = True
                    return True
        self.FCP = False
        return False
    #++++++++++++++++++++++++++++++++++++
    def H_Valid_interface(self):

        if ((self.Description == "") or (self.ID == "0") or (self.config.find("shutdown") != -1)):
            self.Problem = True
        if (self.FCP == False):
            if (self.Profile == "") or (self.DCRM_Profile == "") or (self.DCRM_Profile != self.Profile):
                self.Problem = True
            
        if (self.IP != "") or (self.VPN != "l2VPN") or (self.VPN != "mplsVPN") or (self.VPN != "l3VPN"):
            self.Valid = True
        else:
            self.Valid = False
               
        int_type = self.config.find("isis enable ")
        if int_type != -1:
            self.Type = "ISIS_UpLink"
            return
        int_type = self.config.find("ip binding vpn-instance IPOSS")
        if int_type != -1:
            self.Type = "IPOSS_Uplink"
            return
        int_type = self.config.find("shutdown")
        if  int_type != -1:
            self.Type = "Shut Down"
            return
        int_type = self.config.find("LoopBack")
        int_type2= self.config.find("Loopback") 
        if  int_type != -1 or int_type2 != -1:
            self.Type = "LoopBack"
            return
        int_type = self.config.find("NULL")   
        if  int_type != -1:
            self.Type = "Null"
            return
        int_type = self.config.find("vty")
        if  int_type != -1:
            self.Type = "vty"
            return
    #++++++++++++++++++++++++++++++++++++
    def CR_Valid_interface(self):
        result = False
        a = False
        e = False
      
        if ((self.Description == "no-des") or (self.ID == "0") or (self.config.find("shutdown") != -1)):
            self.Problem = True
        if ((self.FCP == False) and (self.Profile == "")) :
            self.Problem = True
        if ((self.FCP == False) and (self.DCRM_Profile == "")):
            self.Problem = True
        if ((self.FCP == False) and (self.DCRM_Profile != self.Profile)):
            self.Problem = True
            
        Valid = self.config.find("ip router isis")
        if Valid != -1:
            self.Type = "ISIS_UpLink"
            self.Valid = False
            #self.Find_IP()
            return
        Valid = self.config.find("ip binding vpn-instance IPOSS")
        if Valid != -1:
            self.Type = "IPOSS_Uplink"
            self.Valid = False
            #self.Find_IP()
            return
        
        Valid = self.config.find("shutdown")
        if Valid != -1:
            self.Type = "Shut Down"
            self.Valid = False
            return
        Valid = self.config.find("Loopback")
        if Valid != -1:
            self.Type = "LoopBack"
            self.Valid = False  
            return
        Valid = self.config.find("Vlan")   
        if Valid != -1:
            self.Type = "Vlan"
            self.Valid = False
            return 
        Valid = self.config.find("Vlanif")   
        if Valid != -1:
            self.Type = "VlanIF"
            self.Valid = False
            return
             
        a = self.config.find("ip address ") 
        if a != -1 :
            a = True
        e = self.config.find("xconnect")
        if e != -1 :
            e = True
        
        result = a or e
        if result == True:
            self.Valid = True
        else:
            self.Valid = False
        
    #++++++++++++++++++++++++++++++++++++
    def CSW_Valid_interface(self):
        result = False
        a = False
        b = False
        c = False
        d = False
        if ((self.Description == "no-des") or (self.ID == "0") or (self.config.find("shutdown") != -1)):
            self.Problem = True
        if ((self.FCP == False) and (self.Profile == "")) :
            self.Problem = True
        if ((self.FCP == False) and (self.DCRM_Profile == "")):
            self.Problem = True
        if ((self.FCP == False) and (self.DCRM_Profile != self.Profile)):
            self.Problem = True
             
        Valid = self.config.find("ip router isis")
        if Valid != -1:
            self.Type = "ISIS_UpLink"
            self.Valid = False
            return
        Valid = self.config.find("shutdown")
        if  Valid!= -1:
            self.Type = "Shut Down"
            self.Valid = False
            return
        Valid = self.config.find("NULL")   
        if  Valid!= -1:
            self.Type = "Null"
            self.Valid = False
            return
        Valid = self.config.find("vty")
        if  Valid!= -1:
            self.Type = "vty"
            self.Valid = False
            return
        Valid = self.config.find("LoopBack") 
        Valid2= self.config.find("Loopback") 
        if  Valid!= -1 or Valid2 != -1:
            self.Type = "LoopBack"
            self.Valid = False  
            
        Valid = self.config.find("interface Vlan")
        if  Valid!= -1:
            self.Type = "VlanIF"
            self.Valid = False
           
        
        a = self.config.find("switchport access vlan") 
        if a != -1 :
            a = True
        b = self.config.find("switchport trunk allowed vlan")
        if b != -1 :
            b = True
        c = self.config.find("ip address ") 
        if c != -1 :
            c = True
        d = self.config.find("xconnect")
        if d != -1 :
            d = True
        
        result = a or b or c or d  
        if result == True:
            self.Valid = True
        else:
            self.Valid = False
    