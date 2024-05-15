#!/bin/sh

socketfile=gunicorn.socket
servicefile=gunicorn.service
nginxfile="cd_server"

key=$(python3 ./server/secret.py)
devfolder=$(pwd | sed 's/\/[a-zA-Z0-1_-]\+$/\/projects/')

clean() {
  echo "Removing service and socket files, env, and nginx config file"
  rm gunicorn.* .env $nginxfile
  echo "Removing python virtual env"
  rm -rf .venv/
  echo "Permanently removing $devfolder"
  rm -rf $devfolder
}


# Check for proper command line arguments
if [ -z $1 ]
then
  echo "Please provide a username"
  exit 1
elif [ "$1" = "clean" ]
then
  clean
  exit 0
elif [ -z $2 ]
then
  echo "Please provide a domain name or IP"
  exit 1
fi

# Check if we are in the correct location
if ! [ -f ./scripts/setup.sh ]
then
  echo "Navigate to the root of the project to set up."
  exit 1
fi

# Start a venv
if ! [ -d .venv ]
then
  python3 -m venv .venv
else
  echo ".venv found"
fi

if [ "$?" -ne "0" ]
then
  echo "Something went wrong starting a venv..."
fi

# Make a projects folder
mkdir $devfolder

if ! [ -f .env ]
then
  # Write our .env file
  echo FLASK_SECRET_KEY=$key > .env
  echo FLASK_DEV_FOLDER=$devfolder >> .env
else
  echo ".env found"
fi

# Create the gunicorn.socket file
printf "[Unit]\nDescription=Gunicorn socket\n\n" > $socketfile
printf "[Socket]\nListenStream=/run/gunicorn.sock\n\n" >> $socketfile
printf "[Install]\nWantedBy=sockets.target\n" >> $socketfile

# Create the gunicorn.service file
printf "[Unit]\nDescription=Gunicorn daemon\nRequires=gunicorn.socket\nAfter=network.target\n\n" > $servicefile
printf "[Service]\nUser=$1\nGroup=www-data\nWorkingDirectory=$(pwd)\n" >> $servicefile
printf "ExecStart=$(pwd)/.venv/bin/gunicorn \\" >> $servicefile
printf "\n\t--access-logfile - \\" >> $servicefile
printf "\n\t--workers 4 \\" >> $servicefile
printf "\n\t--bind unix:/run/gunicorn.sock \\" >> $servicefile
printf "\n\tserver.main:app \n\n" >> $servicefile
printf "[Install]\nWantedBy=multi-user.target\n" >> $servicefile

# Create nginx config file
printf "server {\n" > $nginxfile
printf "\tlisten 80;\n" >> $nginxfile
printf "\tserver_name $2;\n\n" >> $nginxfile
printf "\tlocation = /favicon.ico { access_log off; log_not_found off; }\n" >> $nginxfile
printf "\tlocation /static/ {\n" >> $nginxfile
printf "\t\troot $(pwd);\n" >> $nginxfile
printf "\t}\n\n" >> $nginxfile
printf "\tlocation / {\n" >> $nginxfile
printf "\t\tinclude proxy_params;\n" >> $nginxfile
printf "\t\tproxy_pass http://unix:/run/gunicorn.sock;\n" >> $nginxfile
printf "\t}\n" >> $nginxfile
printf "}\n" >> $nginxfile


# Additional requirements
echo "NOTE: Manually run the following commands to finish setup."
echo "WARNING: Requires sudo access to write service files.\n"

echo "Load venv and install packages"
echo "  source .venv/bin/activate"
echo "  pip install -r requirements.txt"
echo "  pip install gunicorn\n"

# Copy over the service and config files
echo "Copy service and config files:"
echo "  sudo cp $socketfile $servicefile /etc/systemd/system/"
echo "  sudo cp $nginxfile /etc/nginx/sites-available/\n"

# Start the gunicorn socket
echo "Start gunicorn service:"
echo "  sudo systemctl start gunicorn"
echo "  sudo systemctl enable gunicorn\n"

# Setup nginx
echo "Setup nginx:"
echo "  sudo ln -s /etc/nginx/sites-available/$nginxfile /etc/nginx/sites-enabled"

