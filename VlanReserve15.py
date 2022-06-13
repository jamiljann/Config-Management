from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os
from tkinter.filedialog import askopenfilename, asksaveasfilename

from network_class17 import Network

class my_menus():   
    def __init__(self):   
        self.root = Tk()
        self.PROGRAM_NAME = " Network Automation in TCI-Khorasan "
        self.root.title(self.PROGRAM_NAME)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        dimention = str(screen_width) + 'x' + str(screen_height)
        self.root.geometry(dimention)
        self.root.attributes('-topmost', 1)
        
        style = ttk.Style()
        style.theme_use('clam')
        self.network = None
        self.Search_result = None
        
        self.init_gui()
        
        self.file_frame = Frame(self.root)
        self.search_frame = Frame(self.root)
        self.report_frame = Frame(self.root)

        self.Search_Des_var =   StringVar()
        self.Search_ID_var =    StringVar() 
        self.Search_IP_var =    StringVar()
        self.Search_Port_var =  StringVar()
        self.Search_DSLAM_var=  StringVar()
        self.cnames =           StringVar()  
        self.radio =            StringVar()
        self.Statusmsg=         StringVar()

        self.Tree_router_name =""
        self.Tree_int_name =""
        self.Tree_int_encap =""
        
    def init_gui(self):
        self.create_top_menu()
        self.create_file_menu()
        self.create_search_menu()
        self.create_report_menu()
        self.create_about_menu()
        self.tree = None
            
    def create_file_menu(self):
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Settings",                     menu= self.file_menu)
        self.file_menu.add_command(label="Read Router's Config Files locally.", command= self.ReadConfigsMenu)
        self.file_menu.add_command(label="Open Router's Config Files from the shared folder",  command= self.OpenConfigsMenu)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit",             command= self.exit_app )
    
    def create_search_menu(self):
        self.searchmenu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Search",            menu= self.searchmenu)
        self.searchmenu.add_command(label="DSLAM Gateway",   command= self.CreateGatewayMenu)
        self.searchmenu.add_command(label="ID",              command= self.CreateIDSearchMenu)
        self.searchmenu.add_command(label="Description",     command= self.CreateDesSearchMenu)
        self.searchmenu.add_command(label="IP",              command= self.CreateIPSearchMenu)
        self.searchmenu.add_command(label="Port",            command= self.CreatePortSearchMenu)    

    def create_report_menu(self):
        self.reportmenu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Reports",           menu= self.reportmenu)
        self.reportmenu.add_command(label="Create Report",   command= self.CreateReportMenu)
        
    def create_about_menu(self):  
        self.about_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="About",             menu= self.about_menu)
        self.about_menu.add_command(label="About",           command= self.show_about)

    def create_top_menu(self):
        self.menu_bar = Menu(self.root)
        self.root.config(menu= self.menu_bar)

    def exit_app(self):
        if messagebox.askokcancel("Quit", "Really quit?"):
            self.root.destroy()
        
    def show_about(self):
        about_message = "Network Automation, Version 4.3"
        about_detail = (
            'by Seyedjamil Sabbaghifaragard \n'
            'For assistance please contact the author: \n' 
            'jsabaghi@gmail.com, https://www.linkedin.com/in/seyed-jamil-sabbaghi-faragard/')
        messagebox.showinfo(title='About', message= about_message, detail= about_detail)
        
    def ReadConfigsMenu(self):
        self.tree = None
        self.Hide_All_Frames() 
        self.file_frame.grid(column=0, row=0, padx=8, pady=4)    
        configs_path = "configs/"
        
        try:
            os.listdir(configs_path)
        except Exception as e:
            messagebox.showerror(title='Error', message='Problem Reading Config Files.', detail=str(e) )
            self.Statusmsg.set("Path not OK.\n" + configs_path)
        else:
            self.network = Network()
            self.ListofRouters =  self.network.Router_List()
            self.cnames.set( self.network.Router_List())
            self.Total_Routers = str(self.network.NO_Router())
            self.Statusmsg.set("Reading Config Files...Path is OK. \n" + configs_path)
            
        status_label = Label(self.file_frame, textvariable= self.Statusmsg , fg="green", font="Times 12  bold") #relief=SUNKEN, anchor=W,
        status_label.grid(row=0, column=0, sticky=(W + E), padx=5)
    
    def OpenConfigsMenu(self):
        self.tree = None
        self.Hide_All_Frames() 
        self.file_frame.grid(column=0, row=0, padx=8, pady=4) 
        
        """Open Directory of the Config files."""
        configs_path = filedialog.askdirectory()   
        try:
            os.listdir(configs_path)
        except Exception as e:
            messagebox.showerror(title='Error', message='Problem Reading Config Files.', detail=str(e) )
            self.Statusmsg.set("Path not OK.\n" + configs_path)
        else:
            self.network = Network()
            self.ListofRouters =  self.network.Router_List()
            self.cnames.set( self.network.Router_List())
            self.Total_Routers = str(self.network.NO_Router())
            self.Statusmsg.set("Reading Config Files...Path is OK. \n" + configs_path)
            
        status_label = Label(self.file_frame, textvariable= self.Statusmsg , fg="green", font="Times 12  bold")#relief=SUNKEN, anchor=W,
        status_label.grid(row=0, column=0, sticky=(W + E), padx=5)   
    
    def CreateDesSearchMenu(self):
        self.Hide_All_Frames()   
        self.search_frame.grid(column=0, row=0, padx=8, pady=4)

        Des_label = Label(self.search_frame, text="Input Customer Description:", font="Times 10  bold")
        self.Des_entry = Entry(self.search_frame, textvariable= self.Search_Des_var)
        search_button_Des = Button(self.search_frame, text="Search",   command= self.Description_on_change, bg="orange")
    
        Des_label.grid(row=0, column=0,  padx=5) 
        self.Des_entry.grid(row=1, column=0,  padx=5) 
        self.Des_entry.focus_set()
        search_button_Des.grid(row=2, column=0,  padx=5,  pady=5 )
        
        status_label = Label(self.search_frame, textvariable= self.Statusmsg , fg="green", font="Times 10  bold")#relief=SUNKEN, anchor=W,
        status_label.grid(row=3, column=0, sticky=(W + E), padx=5)
        
    def CreateIDSearchMenu(self):
        self.Hide_All_Frames()    
        self.search_frame.grid(column=0, row=0, padx=8, pady=4)
        
        ID_label = Label(self.search_frame, text="Input Customer ID:", font="Times 10  bold")
        self.ID_entry = Entry(self.search_frame, textvariable= self.Search_ID_var)
        search_button_ID = Button(self.search_frame, text="Search", command= self.ID_on_change, bg="orange")
            
        ID_label.grid(row=0, column=0, sticky=(W + E), padx=5)
        self.ID_entry.grid(row=1, column=0, padx=5)
        self.ID_entry.focus_set()
        search_button_ID.grid(row=2, column=0, padx=5,  pady=5)
        
        status_label = Label(self.search_frame, textvariable= self.Statusmsg , fg="green", font="Times 10  bold")#relief=SUNKEN, anchor=W,
        status_label.grid(row=3, column=0, sticky=(W + E), padx=5)
        
    def CreateIPSearchMenu(self):
        self.Hide_All_Frames()
        self.search_frame.grid(column=0, row=0, padx=8, pady=4)
        
        IP_label = Label(self.search_frame, text="Input Customer IP:", font="Times 10  bold")
        self.IP_entry = Entry(self.search_frame, textvariable= self.Search_IP_var)
        search_button_IP = Button(self.search_frame, text="Search", command= self.IP_on_change, bg="orange")
            
        IP_label.grid(row=0, column=0, sticky=(W + E), padx=5)
        self.IP_entry.grid(row=1, column=0, padx=5)
        self.IP_entry.focus_set()
        search_button_IP.grid(row=2, column=0, padx=5,  pady=5)
        
        status_label = Label(self.search_frame, textvariable= self.Statusmsg , fg="green", font="Times 10  bold")#relief=SUNKEN, anchor=W,
        status_label.grid(row=3, column=0, sticky=(W + E), padx=5)
    
    def CreatePortSearchMenu(self):
        self.Hide_All_Frames()
       
        self.search_frame.grid(column=0, row=0, padx=8, pady=4)
        
        Port_label = Label(self.search_frame, text="Input Customer Port:", font="Times 10  bold")
        self.Port_entry = Entry(self.search_frame, textvariable= self.Search_Port_var)
        search_button_Port = Button(self.search_frame, text="Search", command= self.Port_on_change, bg="orange")
            
        Port_label.grid(row=0, column=0, sticky=(W + E), padx=5)
        self.Port_entry.grid(row=1, column=0, padx=5)
        self.Port_entry.focus_set()
        search_button_Port.grid(row=2, column=0, padx=5,  pady=5)
        
        status_label = Label(self.search_frame, textvariable= self.Statusmsg , fg="green", font="Times 10 ")
        status_label.grid(row=3, column=0, sticky=(W + E), padx=5) 
    
    def CreateReportMenu(self):
        self.Hide_All_Frames()
        self.report_frame.grid(column=0, row=0, padx=8, pady=4) 
        List_label_Text = "Router's List:  " + "( Sum = "+ self.Total_Routers + ")"
        
        List_label = Label(self.report_frame, text= List_label_Text)
        List_label.grid(column=0, row=0, sticky= W , padx=10)
        self.List_entry_search = Entry(self.report_frame, width= 20, font= ("Helvetica", 11))
        self.List_entry_search.bind("<KeyRelease>", self.Checkentry_vs_Listbox)
        self.List_entry_search.grid(column=0, row=1, sticky= W , padx=10, pady=10)
        self.create_list_box(2, 0)
        
        report_button = Button(self.report_frame, text='Generate Report', command = self.Report_on_change, 
                               bg="orange", default='active')
        
        report_button.grid(column=0, row=3, sticky= W, pady=5)
       
        status_label = Label(self.report_frame, textvariable= self.Statusmsg , fg="green", font="Times 10")
        status_label.grid(row=5, column=0, sticky=W , padx=5) 
        
        self.report_frame.grid_columnconfigure(0, weight=1)
        self.report_frame.grid_rowconfigure(5, weight=1)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
    def create_list_box(self, box_row, box_colomn):  
        # Add scroll bar
        self.lbox = Listbox(self.report_frame , listvariable = self.cnames, activestyle='none',
                                cursor='hand2', fg='#1C3D7D', width= 20, height= 10)
        self.lbox.bind("<<ListboxSelect>>", self.ShowRouter)
        self.lbox.grid(row= box_row, column= box_colomn, sticky= W, padx=5)
        scroll_bar = Scrollbar(self.report_frame)
        scroll_bar.grid(row= box_row,column= box_colomn+1, sticky= W)
        
        self.lbox.config(yscrollcommand= scroll_bar.set)
        scroll_bar.config(command= self.lbox.yview)
        self.lbox.selection_set(0)
        
    def Listbox_update(self, data):
        self.cnames.set(list(data))
            
    def Checkentry_vs_Listbox(self, event):
        #grab what was typed
        typed = self.List_entry_search.get()
        if typed == '':
            data = self.cnames
        else:
            data = []
            current_list = self.cnames
            for item in self.network.Router_List():
                if typed.lower() in item.lower():
                    data.append(item)
        self.Listbox_update(data)
        
    def save_file():
        """Save the current file as a new file."""
        filepath = asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],)
        if not filepath:
            return
        with open(filepath, mode="w", encoding="utf-8") as output_file:
            text = txt_edit.get("1.0", tk.END)
            output_file.write(text)
        window.title(f"Simple Text Editor - {filepath}")    
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++           
    def Description_on_change(self):
        """Handle Search button clicks"""
        cus_des = self.Des_entry.get().upper()
        if cus_des != "" :
            result = self.network.Find_Description(cus_des)
            if result:
                self.create_tree(result, self.search_frame, 4,0,20)
            else:
                self.Statusmsg.set("Not Found.")
                for item in self.tree.get_children():
                    self.tree.delete(item)
            
    def ID_on_change(self):
        """Handle Search button clicks"""            
        cus_ID = self.ID_entry.get().upper()
        if cus_ID != "" :
            result = self.network.Find_ID(cus_ID)
            if result:
                self.create_tree(result, self.search_frame, 4,0,20)
            else:
                self.Statusmsg.set("Not Found.")
                for item in self.tree.get_children():
                    self.tree.delete(item)
                    
    def IP_on_change(self):
        """Handle Search button clicks"""
        cus_IP = self.IP_entry.get().upper()
        if cus_IP != "" :
            result = self.network.Find_IP(cus_IP)
            if result:
                self.create_tree(result, self.search_frame, 4,0,20)
            else:
                self.Statusmsg.set( "Not Found.")
                for item in self.tree.get_children():
                    self.tree.delete(item)
                
    def Port_on_change(self):
        """Handle Search button clicks"""            
        cus_Port = self.Port_entry.get().upper()
        if cus_Port != "" :
            result = self.network.Find_Port(cus_Port)
            if result:
                self.create_tree(result, self.search_frame, 4,0,20)
            else:
                self.Statusmsg.set( "Not Found.")
                for item in self.tree.get_children():
                    self.tree.delete(item)
    
    def DSLAM_on_change(self):
        DSLAM_IP = self.DSLAM_entry.get()
        
        status_label = Label(self.search_frame, textvariable= self.Statusmsg , font="Times 10  bold", 
                             fg="green")
        status_label.grid(row=9, column=0, sticky=(W + E), padx=5)
  
        if DSLAM_IP != "" :
            self.Search_result = self.network.Find_Gateway (DSLAM_IP)
            print("Find_Gateway()", self.Search_result)
            if self.Search_result:
                self.Tree_router_name = self.Search_result[0][0]
                self.Tree_int_name = self.Search_result[0][1]
                self.Tree_int_encap = self.Search_result[0][3]
                self.create_tree(self.Search_result, self.search_frame, 3,0,2)
                #self.Search_result = None
                Exist_label = Label(self.search_frame, text="Exist Ports:", font="Times 12 bold")
                Exist_label.grid(row=7, column=0,  padx=5)
                self.Search_result = self.network.List_Gateway_Subports(DSLAM_IP)
                print('List_Gateway_Subports()= ', self.Search_result)
                if self.Search_result:
                        self.create_tree(self.Search_result, self.search_frame, 8,0,15)
                else:
                    self.Statusmsg.set( "There is no result.")
                
                reserve_button_DSLAM = Button(self.search_frame, text="Reserve Port", command= self.Reserve_on_change, bg="orange", fg="black")
                reserve_button_DSLAM.grid(row=10, column=0,  padx=5,  pady=5 ) 
            else:
                self.Tree_router_name = ""
                self.Tree_int_name = ""
                self.Statusmsg.set( "Not Found." )
                for item in self.tree.get_children():
                    self.tree.delete(item)
                
    def Report_on_change(self, *args):
        result = []
        idx = self.lbox.get(ACTIVE) 
        #self.lbox.see(idx)
        self.Statusmsg.set( "Creating Report file ...")
        result= self.network.Show_router_interfaces (idx)
        self.Statusmsg.set( "Report file is Done.")
        if result:
            self.create_tree(result, self.report_frame, 4, 1, 14)
        else:
            self.Statusmsg.set( "There is no result.")

    def ShowRouter(self, event):
        idx = self.lbox.get(ACTIVE)

        this_device_IDs =   self.network.Find_Router(idx).NO_ID()
        this_device_IP  =   self.network.Find_Router_IP(idx)
        this_device_Type  = self.network.Router_Type(idx)
        out_text =  "Exist IDs = "+ str(this_device_IDs) + "\n  IP: "+ str(this_device_IP) + "\n  Type: "+ str(this_device_Type)
        self.Statusmsg.set( out_text)
         
    def create_tree(self, result, frame_name, row_num, column_num, Height):
        columns = ('router', 'interface', 'description', 'encap', 'ID', 'IP', 'VPN', 'profile', 'RM_Profile')
        
        self.tree = ttk.Treeview(frame_name, height= Height, columns= columns, show='headings')
        # define headings
        self.tree.heading('router',         text='Router',          anchor=CENTER)
        self.tree.heading('interface',      text='Interface',       anchor=W)
        self.tree.heading('description',    text='Description',     anchor=W)
        self.tree.heading('encap',          text='Encapsulation',   anchor=W)
        self.tree.heading('ID',             text='Customer ID',     anchor=CENTER)
        self.tree.heading('IP',             text='IP',              anchor=CENTER)
        self.tree.heading('VPN',            text='VPN',             anchor=W)
        self.tree.heading('profile',        text='Profile',         anchor=W)
        self.tree.heading('RM_Profile',     text='Int Type',        anchor=W)
        
        self.tree.column('router',          width=140,       anchor=CENTER)
        self.tree.column('interface',       width=160,       anchor=CENTER)
        self.tree.column('description',     width=210,       anchor=CENTER)
        self.tree.column('encap',           width=80,        anchor=CENTER)
        self.tree.column('ID',              width=75,        anchor=CENTER)
        self.tree.column('IP',              width=150,       anchor=CENTER)
        self.tree.column('VPN',             width=80,        anchor=CENTER)
        self.tree.column('profile',         width=50,        anchor=CENTER)
        self.tree.column('RM_Profile',      width=70,        anchor=CENTER)
        
        for searched_result in result:
            self.tree.insert('', END , values= searched_result )
        #self.tree.bind('<<self.treeviewSelect>>', item_selected)
        self.tree.grid( row=row_num, column= column_num, sticky= NSEW)
        # add a scrollbar
        scrollbar = ttk.Scrollbar(frame_name, orient=VERTICAL, command= self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row= row_num, column= column_num+1, sticky=NSEW)
        #return self.tree
        output_number = len(self.tree.get_children())
        self.Statusmsg.set( "Number Of Records= "+ str(output_number))
        
        self.tree.bind('<Key-Return>', self.print_contents)
        self.tree.bind('<<TreeviewSelect>>', self.tree_item_selected)
    
    def print_contents(self, event):
        messagebox.showinfo('Full Interface Configuration',"Must show all Interface configs")
    
    def tree_item_selected(self, event):
        result = ""
        for selected_item in self.tree.selection():
            item = self.tree.item(selected_item)
            Tree_router_name =  item['values'][0]
            Tree_int_name =     item['values'][1]
            result = self.network.Show_int_config(Tree_router_name, Tree_int_name) 
            # show a message
            messagebox.showinfo(self.PROGRAM_NAME, result)
                        
    def Hide_All_Frames(self):
        self.Statusmsg.set("")
        if self.tree is not None:
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.tree.grid_forget() 
        # destroy all widgets from search_frame
        if self.search_frame is not None:
            for widget in self.search_frame.winfo_children():
                widget.destroy()
            self.search_frame.grid_forget()                  
        # destroy all widgets from report_frame
        if self.report_frame is not None:
            for widget in self.report_frame.winfo_children():
                widget.destroy()
            self.report_frame.grid_forget()       
        # destroy all widgets from file_frame
        if self.file_frame is not None:
            for widget in self.file_frame.winfo_children():
                widget.destroy()
            self.file_frame.grid_forget() 
        
    
    def CreateGatewayMenu(self):
        self.Hide_All_Frames() 
        
        self.search_frame.grid(column=0, row=0, padx=8, pady=4)
        
        DSLAM_label = Label(self.search_frame, text="Input DSLAM IP:", font="Times 10 bold")
        self.DSLAM_entry = Entry(self.search_frame, textvariable= self.Search_DSLAM_var)
        search_button_DSLAM = Button(self.search_frame, text="Find Gateway",   command= self.DSLAM_on_change, bg="orange")
    
        DSLAM_label.grid(row=0, column=0,  padx=5) #sticky=(tk.W + tk.E),
        self.DSLAM_entry.grid(row=1, column=0,  padx=5) 
        self.DSLAM_entry.focus_set()
        search_button_DSLAM.grid(row=2, column=0,  padx=5,  pady=5 )  
        
    def Reserve_on_change(self):
        result = []
        if self.Tree_router_name != "": 
            result = self.network.List_Gateway_Subports(self.Tree_router_name, self.Tree_int_name )
            if result:
                    self.create_tree(result, self.search_frame, 6,0,15)
            else:
                self.Statusmsg.set( "There is no result.")

       
    

if __name__ == '__main__': 
    My_menu = my_menus()
    My_menu.root.mainloop()