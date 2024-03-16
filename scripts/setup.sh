#!/bin/sh

socketfile=gunicorn.socket
servicefile=gunicorn.service

servicedir=/etc/systemd/system/

key=$(python3 ./server/secret_key.py)
devfolder=$(pwd | sed 's/\/[a-zA-Z0-1_-]\+$/\/projects/')

clean() {
  rm gunicorn.* .env
  rm -rf .venv/
  rmdir $devfolder
}


# Check for proper command line arguments
if [ -z $1 ]
then
  echo "Please provide a username."
  exit 1
elif [ "$1" = "clean" ]
then
  clean
  exit 0
fi

# Check if we are in the correct location
if ! [ -f ./scripts/setup.sh ]
then
  echo "Navigate to the root of the project to set up."
  exit 1
fi

# Start a venv
python3 -m venv .venv

if [ "$?" -ne "0" ]
then
  echo "Something went wrong starting a venv..."
fi

# Make a projects folder
mkdir $devfolder

# Write our .env file
echo FLASK_SECRET_KEY=$key > .env
echo FLASK_DEV_FOLDER=$devfolder >> .env

# Create the gunicorn.socket file
printf "[Unit]\nDescription=gunicorn socket\n\n" > $socketfile
printf "[Socket]\nListenStream=/run/gunicorn.sock\n\n" >> $socketfile
printf "[Install]\nWantedBy=sockets.target\n" >> $socketfile

# Create the gunicorn.service file
printf "[Unit]\nDescription=gunicorn daemon\nRequires=gunicorn.socket\nAfter=network.target\n\n" > $servicefile
printf "[Service]\nUser=$1\nGroup=www-data\nWorkingDirectory=$(pwd)\n" >> $servicefile
printf "ExecStart=$(pwd)/.venv/bin/gunicorn \\" >> $servicefile
printf "\n\t--access-logfile - \\" >> $servicefile
printf "\n\t--workers 4 \\" >> $servicefile
printf "\n\t--bind unix:/run/gunicorn.sock \\" >> $servicefile
printf "\n\tserver.serve:app \n\n" >> $servicefile
printf "[Install]\nWantedBy=multi-user.target\n" >> $servicefile


# Additional requirements
echo "NOTE: Please load venv and install packages"
echo "  source .venv/bin/activate"
echo "  pip install -r requirements.txt"
echo "  pip install gunicorn"

# Copy over the service files
echo "WARNING: Requires sudo access to write service files."
echo "  sudo cp $socketfile $servicefile $servicedir\n"

# Start the gunicorn socket
echo "Start gunicorn service with:"
echo "  sudo systemctl start gunicorn.socket"
echo "  sudo systemctl enable gunicorn.socket"

