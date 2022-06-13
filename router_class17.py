import xlwt
import xlrd 

from os import path
from interface_class17 import Interface

class Router():    
    def __init__(self, file_name):        
        self.Name = file_name.split('.cfg')[0]
        self.file_name = str(path.realpath('configs'))+ '/' + file_name
        self.Type = ""
        self.IP = ""
        self.all_interfaces = [] 
        self.NO_Ints = 0
        self.No_IDs = 0
        
        self.Set_Type()
        self.Create_Interfaces()
        self.SetIP_Profile_Valid()
        
    #++++++++++++++++++++++++++++++++++++
    def Set_Type(self): 
        if ((self.Name.find("nPE")!= -1) or (self.Name.find("7609")!= -1) or (self.Name.find("7507")!= -1) or 
            (self.Name.find("ASR")!= -1)):
            self.Type = "Cisco_R"
        if ((self.Name.find("NAR")!= -1)  or (self.Name.find("9300")!= -1) or (self.Name.find("PRR")!= -1) or 
            (self.Name.find("SER")!= -1)  or (self.Name.find("NRR")!= -1)  or (self.Name.find("2300")!= -1) or
            (self.Name.find("5328")!= -1) or (self.Name.find("ME60")!= -1) or (self.Name.find("2811")!= -1) or 
            (self.Name.find("4620")!= -1) or (self.Name.find("4680")!= -1) or (self.Name.find("5300")!= -1)):
            self.Type = "Huawei"  
        if ((self.Name.find("3750")!= -1) or (self.Name.find("2960")!= -1)  or (self.Name.find("6524")!= -1) or 
            (self.Name.find("3550")!= -1) or (self.Name.find("3560")!= -1)  or (self.Name.find("3850")!= -1) or 
            (self.Name.find("3600")!= -1) or (self.Name.find("12S")!= -1)):
            self.Type = "Cisco_SW"
            
    #++++++++++++++++++++++++++++++++++++
    def Create_Interfaces(self):
        config_lines = ""
        interface = 0
        count=0
        
        with open(self.file_name, 'r', encoding='utf-8') as f:
            if self.Type == "Cisco_R" or self.Type == "Cisco_SW":     
                for line in f.readlines():
                    if line.find("interface") == 0:
                        config_lines = config_lines + line 
                        interface = 1
                        count=0
                        count += 1
                    elif line.find("!") != -1 :
                        if interface == 1:
                            self.all_interfaces.append(Interface(config_lines))
                            config_lines =""
                            interface = 0
                    elif interface == 1 and count < 25:
                        config_lines = config_lines + line 
                        count += 1
                    else:
                        continue    
            elif self.Type == "Huawei":
                for line in f.readlines():
                    if line.find("interface") == 0:
                        config_lines = config_lines + line 
                        interface = 1
                        count=0
                        count += 1
                    elif line.find("#") != -1 :
                        if interface == 1:
                            self.all_interfaces.append(Interface(config_lines) )
                            config_lines =""
                            interface = 0
                    elif interface == 1 and count < 25:
                        config_lines = config_lines + line 
                        count += 1
                    else:
                        continue   
            else:
                print('Unknown Router= ', self.file_name )
        
    #++++++++++++++++++++++++++++++++++++
    def SetIP_Profile_Valid(self):
        ''' Set Router's IP , 
            Port's Encapsulation, Profile, Type, Valid, Problem'''
        for ints in self.all_interfaces:
            self.NO_Ints += 1
            if ints.ID != "0":
                self.No_IDs +=1
                    
            if self.Type.find("Huawei")!= -1:
                ints.Find_H_profile()
                ints.H_Valid_interface()
                
            elif self.Type.find("Cisco_R")!= -1:
                ints.Find_CR_profile()
                ints.CR_Valid_interface()
                
            elif self.Type.find("Cisco_SW")!= -1:
                ints.Find_CR_profile()
                ints.CSW_Valid_interface()
            else:
                self.Type == "Other"
                
            if (ints.Type == "ISIS_UpLink") or (ints.Type == "IPOSS_Uplink") :
                self.IP = ints._Return_IP()
            elif (ints.Type == "Vlan") and (ints.Description == "MANAGE") :
                self.IP = ints._Return_IP()
            elif ints._Return_IP().find("172.21") != -1:
                self.IP = ints._Return_IP()
    #++++++++++++++++++++++++++++++++++++           
    def NO_ID(self): 
        return(self.No_IDs)
    #++++++++++++++++++++++++++++++++++++           
    def NO_Int(self): 
        return(self.NO_Ints)
    #++++++++++++++++++++++++++++++++++++           
    def _Router_IP(self): 
        return(self.IP)
    #++++++++++++++++++++++++++++++++++++           
    def Find_Description(self, my_Des):
        result = []

        for ints in self.all_interfaces:
            interface_result = ints.Find_Description(my_Des, self.Name)
            if interface_result :
                result.append (interface_result)          
        if result == [] :         
            return False
        else:
            return result

    #++++++++++++++++++++++++++++++++++++   
    def Find_ID(self, my_ID):
        result = []
        if my_ID.isnumeric():
            for ints in self.all_interfaces:
                id_result = ints.Find_ID(my_ID, self.Name)
                if id_result :
                    result.append (id_result)          
        if result == [] :         
            return False
        else:
            return result
        
     #++++++++++++++++++++++++++++++++++++   
    def Find_IP(self, my_IP):
        result = []

        for ints in self.all_interfaces:
            IP_result = ints.Find_IP(my_IP, self.Name)
            if IP_result :
                result.append (IP_result)          
        if result == [] :         
            return False
        else:
            return result
        
    #++++++++++++++++++++++++++++++++++++   
    def Find_Port(self, int_name):
        result = []

        for ints in self.all_interfaces:
            Name_result = ints.Find_Port(int_name, self.Name)
            if Name_result :
                result.append (Name_result)          
        if result == [] :         
            return False
        else:
            return result 
        
    #++++++++++++++++++++++++++++++++++++   
    def Show_Interfaces(self, interface_Name = None):
        result = []

        for ints in self.all_interfaces:
            if interface_Name is not None:
                if ints.Name != interface_Name:
                    continue
            Name_result = ints.Show_Interface(self.Name) 
            if Name_result :
                result.append (Name_result)
        if result == [] :         
            return False
        else:
            return result 
        
    #++++++++++++++++++++++++++++++++++++  
    def Find_Free_Ports(self):
        result = []
        for ints in self.all_interfaces:
            IP_result = ints.Find_Free_Ports(self.Name) 
            if IP_result :
                result.append(IP_result)
        if result == [] :         
            return False
        else:
            return result
        
    #++++++++++++++++++++++++++++++++++++   
    def Find_IP_INET(self):
        result = []
        for ints in self.all_interfaces:
            if ints.Find_IP_INET() :
                result.append(ints.Show_Interface(self.Name))
        if result == [] :         
            return False
        else:
            return result   
    #+++++++++++++++++++++++++++++++++++"
    def Same_PE_Ints(self, int_name, int_ecap):
        result = []
        output = []
        find = False

        first_port_name = int_name.split(".")[0]
        port_pe = int(int_ecap[1].strip()) 
        '''first_port_name = Interface Name to dot'''
        result = self.Find_Port(first_port_name)
        '''Find all interfaces start with first_port_name'''
        for item in result:
            find = False
            for encap_item in item[3]:
                if encap_item.isnumeric(): 
                    if port_pe == int(encap_item):
                        find = True
                        continue
                    if find:
                        output.append (item)
        '''return a list of show_port, Return PE'''
        return(output, port_pe)   
       
    #+++++++++++++++++++++++++++++++++++"              
    def Write_To_File(self, file_name, write_text):
        try:
            with open(file_name, 'w') as f:
                f.write(write_text)
        except Exception as e:
            print(e)
    #+++++++++++++++++++++++++++++++++++"              
    def Write_Config_Summary(self):
        write_text =''
        for item in self.all_interfaces:
            write_text = write_text + item.config

        file_name = str(path.realpath('SumConfigs'))+ '/'+ self.Name + '.txt'
        self.Write_To_File(file_name, write_text)
            
    #++++++++++++++++++++++++++++++++++++
    def Export_interfaces_excel(self):  
        '''create Excel file to show all Interfaces of Router...'''
        i =1
        my_workbook = xlwt.Workbook()
        sheet = my_workbook.add_sheet(self.Name)
        sheet.write(0, 0, 'نام تجهیز')
        sheet.write(0, 1, 'شماره پورت')
        sheet.write(0, 2, 'نام مشترک')
        sheet.write(0, 3, 'شماره پرونده')
        sheet.write(0, 4, 'VPN')
        sheet.write(0, 5, 'Encapsulation')
        sheet.write(0, 6, 'Qos Exist')
        sheet.write(0, 7, 'Qos-DCRM')
        sheet.write(0, 8, 'Type')
        sheet.write(0, 9, 'Valid')
        sheet.write(0, 10, 'FCP')
        sheet.write(0, 11, 'Problem')
        sheet.write(0, 12, 'IP')
        
        for ints in self.all_interfaces:
            sheet.write(i, 0, self.Name)
            sheet.write(i, 1, ints.Name)
            sheet.write(i, 2, ints.Description)
            sheet.write(i, 3, ints.ID)
            sheet.write(i, 4, ints.VPN)
            sheet.write(i, 5, ints.Encap)
            sheet.write(i, 6, ints.Profile)
            sheet.write(i, 7, ints.DCRM_Profile)
            sheet.write(i, 8, ints.Type)
            sheet.write(i, 9, ints.Valid)
            sheet.write(i, 10, ints.FCP)
            sheet.write(i, 11, ints.Problem)
            sheet.write(i, 12, ints.IP)

            i +=1 
        file_name = "Reports/Ports-of-" + self.Name + ".xls"
        my_workbook.save(file_name)
    #++++++++++++++++++++++++++++++++++++
    def Export_Valid_interfaces(self):      
        i =1
        my_workbook = xlwt.Workbook()
        sheet = my_workbook.add_sheet("Port-Problems")
        sheet.write(0, 0, 'نام تجهیز')
        sheet.write(0, 1, 'شماره پورت')
        sheet.write(0, 2, 'نام مشترک')
        sheet.write(0, 3, 'شماره پرونده')
        sheet.write(0, 4, 'Encapsulation')
        sheet.write(0, 5, 'Qos Exist')
        sheet.write(0, 6, 'Qos-DCRM')
        sheet.write(0, 7, 'Type')
        sheet.write(0, 8, 'FCP')
        sheet.write(0, 9, 'Problem')
        
        for ints in self.all_interfaces:
            if ints.Valid:
                sheet.write(i, 0, self.name)
                sheet.write(i, 1, ints.Name)
                sheet.write(i, 2, ints.Description)
                sheet.write(i, 3, ints.ID)
                sheet.write(i, 4, ints.Encap)
                sheet.write(i, 5, ints.Profile)
                sheet.write(i, 6, ints.DCRM_Profile)
                sheet.write(i, 7, ints.Type)
                sheet.write(i, 8, ints.FCP)
                sheet.write(i, 9, ints.Problem)
                i +=1 
        file_name = "Valid-Ports-of-" + self.name + ".xls"
        my_workbook.save(file_name)
        '''create Excel file to show Valid Interfaces of Router...")'''
  
