from flask import Flask,render_template,url_for,send_from_directory,request,redirect,flash

from main_action import PlaybookCreator as Playbook
from zipfile import ZipFile
import os
app = Flask(__name__)
app.secret_key = "abc"


playbook = Playbook()
project_name = ""
@app.route("/",methods=['GET'])
def index():    
    return render_template("index.html")

@app.route("/newproject",methods=['POST'])
def create_project():
    global project_name
    project_name = request.form.get("project_name")
    project_name = project_name.replace(" ","")
    status = playbook.create_project(project_name)
    if status == True:        
        flash("project created")
        return redirect(url_for("tasks"))
    else:
        flash("failed to project created")
        return redirect(url_for("index"))
    
@app.route("/tasks",methods=['POST','GET'])
def tasks():
    if request.method == 'GET':
        return render_template("tasks.html")
    elif request.method == 'POST':
        tasks = []
        task = []
        task_names = request.form.getlist("task_name[]")
        task_type = request.form.getlist("task_type[]")
        module_name = request.form.getlist("module_name[]")
        status = request.form.getlist("status[]")
        
        for i in range(len(task_names)):
            task.append(task_names[i])
            task.append(task_type[i])
            task.append(module_name[i])
            task.append(status[i])
            if task[0] !="":
                tasks.append(task)
                task = []
            else:
                flash("please enter task to be included to playbook")
                return redirect(url_for("tasks"))
        try:
            
            playbook.create_task(tasks)
            playbook.save_playbook()
            
            #zipping the project
            file_paths = []
  
            # crawling through directory and subdirectories
            for root, directories, files in os.walk(project_name):
                for filename in files:
                    # join the two strings in order to form the full filepath.
                    filepath = os.path.join(root, filename)
                    file_paths.append(filepath)
            global zippedproject
            
            zippedproject = project_name+".zip"
            with ZipFile(zippedproject,'w') as zip:
            # writing each file one by one
                for file in file_paths:
                    zip.write(file)
        except:
            return "Failed to create the playbook, try again"
            
        return redirect(url_for("download"))
    
@app.route('/download',methods=['GET'])
def download():
    if request.method == 'GET':
        project = zippedproject
        return render_template("download.html",project=project)
    else:
        return redirect("unsupported request") 
    
@app.route('/download/playbook/<filename>',methods=['GET'])
def download_playbook(filename):
    if request.method == 'GET':
        #uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
        return send_from_directory('.', filename=filename)
    else:
        return redirect("unsupported request")       

if __name__ == "__main__":
    pass
app.run(debug=True)