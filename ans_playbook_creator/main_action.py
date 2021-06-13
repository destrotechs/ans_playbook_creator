"""all playbook manipulation and creation are done here,

    morris destro:
"""

import os
class PlaybookCreator:
    dir_path = ""
    status = True
     
    def __init__(self):
        self.cients = set()
       
    def create_project(self,project_name):
        self.project_name = project_name
         #create the project directory
        try:
            print("[creating project directory] *****************************")
            os.system(f"mkdir {self.project_name}")
            print("[project created]")
            return True
        except:
            PlaybookCreator.status = False            
            print("project directory could not be  created use a proper name ...")
            return False
    def create_task(self,tasks):
       self.tasks = tasks
    #set the repository manager// apt or yum
    def task_install_module(self,package_manager,module):
        self.modules.add(module)
        self.package_manager = package_manager
    def create_clients(self,client_address):
        self.clients.add(client_address)
    def task_services(self,service,operation):
        self.services.add(service)
        self.services_operations.append(operation)
    def save_playbook(self):
        #create a file on the project dir
        try:
            print("*****Trying to create tasks****")
            playbook = open(self.project_name+"/playbook.yml","a")
            
            #write the content to the file
            playbook.write("---")
            
            playbook.write("\n- name: "+self.project_name)
            playbook.write("\n  hosts: ansible_clients")
            playbook.write("\n  remote_user: root")
            playbook.write("\n  become: true")
            playbook.write("\n\n")
            
            playbook.write("  tasks:")
            
            if len(self.tasks)>0:
                for task in self.tasks:
                    playbook.write("\n   - name: "+task[0])
                            
                    try:
                        
                        if task[1] == "service":                            
                            playbook.write("\n     "+task[1]+":\n")
                            playbook.write("      name: "+task[2])
                            playbook.write("\n      status: "+task[3])
                        elif task[1] == "apt" or task[1]=="yum":
                            playbook.write("\n    "+task[1]+":\n")
                            playbook.write("      name: "+task[2])
                            playbook.write("\n      status: "+task[3])     
                        elif task[1] == "copy":
                            playbook.write("\n     "+task[1]+":\n")
                            playbook.write("       content: "+task[2])
                            playbook.write("\n       dest: "+task[3])
                            
                    except:
                            print("Error while adding tasks to playbook")
                print("*****Tasks added to playbook successfully ****")
            else:
                print("No tasks to add to playbook")
        except:
            print("Playbook could not be written, unrecognized tasks found")
            
        #save the file
        
        #zip the directory
        
    