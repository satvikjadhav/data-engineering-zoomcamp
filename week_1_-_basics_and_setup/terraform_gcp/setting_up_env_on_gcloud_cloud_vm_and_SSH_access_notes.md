## Setting up Google Cloud Virtual Machine (VM)
	- Renting an instance or a virtual machine and many other resources. 

Can be found under Compute Engine -> VM Instance

### Before we make an instance, we need to make an SSH Key. 
	- This Key will be used to log in to the instance that we will be using/making.
	- We can use GIT Bash to do this as SSH is already built into GIT Bash. 
	- https://cloud.google.com/compute/docs/connect/create-ssh-keys
	- ssh-keygen -t rsa -f ~/.ssh/KEY_FILENAME -C satvikjadhav -b 2048
		- Run this in the GIT Bash console to generate the ssh key
		- we can leave the passphrase empty if wanted
		- This will create two keys: one public, and one private
		- We now put this public key generated to our google cloud
			- Metadata
			- SSH keys
			- Add
		- Once added, all instances in the project we are in will inherit the SSH keys that we add (could be more than one)

We can also change the boot disk of the Virtual Machine (VM) we are spinning up. 

We can also create a VM instance by using the "EQUIVALENT COMMAND LINE" option. 
This will be done via the gcloud sdk that we had installed earlier

Once this VM is created, we are no interested in the external ip that is associated with the respective VM. 

### Now, we do the following steps:
	1. We go to the git bash console, and enter: ssh -i ~/.ssh/gpc satvikjadhav@35.244.13.10
		- i: identity
		- use the the private key file
		- Name we used to generate the key
		- last step is the external url

	2. Using the "htop" command we can see the machine config

### Once we have access to our VM, we now need to configure it.

	1. We will first get anaconda
		- we will download anaconda into our vm
		- wget https://repo.anaconda.com/archive/Anaconda3-2021.11-Linux-x86_64.sh
		- bash Anaconda3-2021.11-Linux-x86_64.sh

	2. Now we create a file called config in the .ssh folder in our local computer
		- command: touch config
		- in this config file we want to configure the access to our VM
		- Host de-test
			HostName 35.244.13.10
			User satvikjadhav
			IdentityFile ~/.ssh/gpc

			- Host: same name as our VM instance name
			- HostName: External IP
			- User: Name we used to create the SSH key
			- IdentityFile: where the file is stored

	3. We can see the bashrc using "less .bashrc" command

	4. If you don't want to log out and log in again:
		- source .bashrc

	5. Now that we have python, lets install docker.
		- sudo apt-get update
		- sudo apt-get install docker.io

	6. Clone the course repo from your git hub to the VM
		- For example: git clone https://github.com/satvikjadhav/data-engineering-zoomcamp.git
		- Configure your GitHub account:
			- git config --global user.email "you@example.com"
			- git config --global user.name "Your Name"
		- once we do git push, we will be asked to input out git hub account user name and password
		- for password we cannot use your github account password as github as stopped supporting it. 
		- Instead we need to create a Personal Access Token (PAT)
			- Settings
			- Developer Settings
			- Personal Access Token
			- Generate New Token

	7. Docker
		- running "docker run hello-world" will give an error
		- This is because we need to give it permissions
		- Follow the guide here: https://github.com/sindresorhus/guides/blob/main/docker-without-sudo.md
		- docker run -it ubuntu bash
		- and we now have docker in our VM

	8. Docker-Compose
		- We download docker compose
			- Go to docker-compose github page and select the latest release on the right side
			- select the linux-x86_64 (make sure it matches the architecture of your VM)
			- mkdir bin (this is where we will store all our executable files)
			- wget https://github.com/docker/compose/releases/download/v2.2.3/docker-compose-linux-x86_64 -O docker-compose
				- O: specifying the output
			- to give make this file executable:
				- chmod +x docker-compose
					- chmod: change mode
			- ./docker-compose version -- to check the version

		- Now we want to make this visible not just in the bin directory but also in any directory
			- using nano .bashrc file to open bashrc file
			- now we will add the bin directory to our path
			- export PATH="${HOME}/bin:${PATH}"
			- Buy doing this we can run docker-compose from anywhere
		
		- now we go in our docker_sql file in our repo
			- docker-compose up -d
				- d: run it in detached mode
			- now docker will add the images for pgadmin4 and postgres 13 as specified in the docker-compose.yaml file

		- Now lets install pgcli
			- pip install pgcli
			- we might get a few errors but it will try all the versions untill one works

			- Lets try this now with conda
				- conda install -c conda-forge pgcli 
				- when installing from conda, it downloads an already compiled version of pgcli
				- if we get the following error:
					- ImportError: cannot import name 'DynamicCompleter' from 'prompt_toolkit.completion'
				- Then do the following:
					- pip install -U mycli

	9. How to access the postgres port
		- postgres from docker is running on the port 5432
		- We would like to forward this port to our local machine so that we can interact with postgres instance locally
		- in visual studios, we can use ctrl + ~ to access  the ports section
			- and click forward port button and forward 5432 and 8080 ports
			- we can now access the postgres instance from our local machine
			- and we can access pgadmin via the web browser  

	10. How to start jupyter
		- We would need to forward port 8888 to be able to access jupyter notbook website
		- we would also need to download the data (rides csv files) into our vm
			- wget url_to_csv_files

	11. Installing terraform
		- https://www.terraform.io/downloads
		- select linux
		- we want to just download the binary (but we can use the package manager too)
		- Linux binary download: amd64, copy the url
		- and download it into our bin directory in VM
		- Since this is a zip file, we want to unzip it
			- install unzip: sudo apt-get install unzip
			- unzip terraform_1.1.4_linux_amd64.zip
	
	12. Uploading files to VM
		- if we want to use terraform in our vm, we would require our google cloud credentials
		- to upload the credentials file we can use Secure File Transfer Protocol (SFTP)
		- command: sftp de-test (our VM's name) <- using this to connect to our vm
		- we can make a directory called .gc where we will put the file
			- mkdir .gc
		- put credential_file_name.json

	13. Setting up gcloud in our VM
		- create an env variable called GOOGLE_APPLICATION_CREDENTIALS
			- export GOOGLE_APPLICATION_CREDENTIALS=~/.gc/credentials_file_name.json
		- we now use this json file to authenticate our cli
		- gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS
		- we can now use terraform commands to initiate GCP resources, and destroy them
		- project id is our project id from gcp
	
