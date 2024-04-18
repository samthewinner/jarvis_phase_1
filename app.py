from flask import Flask,render_template,request,make_response,redirect,url_for
import subprocess

app = Flask(__name__)

containers = ['loose_rock','empty_rock','dilligent_pig','might_rope','timid_shadow']
containers = [[x,True] for x in containers]
headings = ['Container name','Run/Stop','Delete']

def get_running_containers():
    try:
        # Run the 'docker ps' command and capture the output
        result = subprocess.run(['docker', 'ps','-a', '--format', '{{.Names}}'], capture_output=True, text=True)
        #TODO return the status of the container along with name
        
        # Check if the command executed successfully
        if result.returncode == 0:
            # Split the output by newline to get individual container names
            container_names = result.stdout.strip().split('\n')
            return container_names
        else:
            print("Error:", result.stderr)
            return None
    except Exception as e:
        print("An error occurred:", e)
        return None
    
@app.route('/create_dockerfile',methods=['POST','GET'])
def create_dockerfile():
     
    prompt = dict(request.form)['dockerfile_prompt']
    
    dockerfile_content = """
    # Use the official Python image from Docker Hub
    FROM python:3.9-slim

    # Set the working directory inside the container
    WORKDIR /app

    # Copy the current directory contents into the container at /app
    COPY . /app

    # Install any needed dependencies specified in requirements.txt
    # If you don't have any dependencies, you can omit this step
    COPY requirements.txt /app
    RUN pip install --no-cache-dir -r requirements.txt

    # Command to run the Python script when the container starts
    CMD ["python", "app.py"]
    """

    # file_path = "./Dockerfile"
    # create_dockerfile(file_path,dockerfile_content,form['dockerfile_prompt'])
    # running_containers = get_running_containers()

    # Write the Dockerfile content to the specified file path
    # with open(file_path, 'w') as f:
    #     f.write(dockerfile_content)
    print(f"id from create is {prompt}")
    containers.append([prompt,True])    
    print(containers)
    return render_template('docker_UI.html',data=containers,headings=headings)
    
    


def ssh_connection(client_passwd,client_uname,client_ip):
    

    # client_passwd = "changeme"
    # client_ip = "192.168.1.8"
    # client_uname = "samarth"
    command = [
        "sshpass",
        "-p", client_passwd,
        "ssh", "-o", "stricthostkeychecking=no",
        f"{client_uname}@{client_ip}",
        "cat ip.txt"
    ]
    op = subprocess.run(command, text=True)
    

@app.route('/stop_container',methods=['POST','GET'])
def stop_container():
    # print("inside stop")
    req_data = request.get_json()
    print(req_data['id'])
    for i in range(len(containers)):
        if containers[i][0] == req_data['id']:
            containers[i][1] = False
            
            #command = ["docker","stop",f"{container_name}"]
            #subprocess.run(command,text=True)

    # print(containers)
    
          
    return render_template('docker_UI.html',data=containers,headings=headings)

@app.route('/run_container',methods=['POST','GET'])
def run_container():
    # print("inside run")
    req_data = request.get_json()['id']
    for i in range(len(containers)):
        if containers[i][0] == req_data:
            containers[i][1] = True
            
            #command = ["docker","stop",f"{container_name}"]
            #subprocess.run(command,text=True)
    return render_template('docker_UI.html',data=containers,headings=headings)

@app.route('/deleted',methods=['GET'])
def deleted():
    print('inside deleted')
    return  render_template('docker_UI.html',data=containers,headings=headings)

@app.route('/delete_container',methods=['POST','GET'])
def delete_container():
    id = request.get_json()['id']
    print(f"id from delete is {id}")
    # command = ["docker","rm","-f",f"{container_name}"]
    for i in containers:
        if i[0] == id:
            containers.remove(i)
            # break
    print(containers)
    # return render_template('docker_UI.html',data=containers,headings=headings)
    return redirect(url_for('deleted'),code=303)
    
def docker(form):

    
    
    return render_template('docker_UI.html',data=containers,headings=headings)

@app.route('/get_host_details',methods=['POST','GET'])
def get_host_details():
    form = request.form.to_dict()
    
    #ssh into host 
    # ssh_connection(form['password'],form['userName'],form['ip'])
    

    return docker(form)

@app.route('/',methods=['GET','POST'])
def hello():
    
    # print(f"Dockerfile created at: {file_path}")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)


