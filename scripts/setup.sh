#!/bin/sh

if [ -z $1 ]
then
  echo "Please provide a username."
  exit 1
fi

if ! [ -f ./scripts/setup.sh ]
then
  echo "Navigate to the root of the project to set up."
  exit 1
fi

python3 -m venv .venv

key=$(python3 ./src/secretkey.py)
devfolder=$(pwd | sed 's/\/[a-zA-Z0-1_-]\+$/\/projects/'])

mkdir $devfolder

echo FLASK_SECRET_KEY=$key > .env
echo FLASK_DEV_FOLDER=$devfolder >> .env

echo "WARNING: Requires sudo access to write service files."

socketfile=gunicorn.socket
servicefile=gunicorn.service

servicedir=/etc/systemd/system/

printf "[Unit]\nDescription=gunicorn socket\n\n" > $socketfile
printf "[Socket]\nListenStream=/run/gunicorn.sock\n\n" >> $socketfile
printf "[Install]\nWantedBy=sockets.target\n" >> $socketfile

printf "[Unit]\nDescription=gunicorn daemon\nRequires=gunicorn.socket\nAfter=network.target\n\n" > $servicefile
printf "[Service]\nUser=$1\nGroup=www-data\nWorkingDirectory=$path\n" >> $servicefile
printf "ExecStart=$path/.venv/bin/gunicorn" >> $servicefile
printf "\n\t--access-logfile - \\" >> $servicefile
printf "\n\t--workers 4 \\" >> $servicefile
printf "\n\t--bind unix:/run/gunicorn.sock \\" >> $servicefile
printf "\n\tsrc/main:app \n\n" >> $servicefile

printf "[Install]\nWantedBy=multi-user.target\n" >> $servicefile

sudo cp $socketfile $servicedir
sudo cp $servicefile $servicedir

echo "NOTE: Please load venv and install packages"
echo "  source .venv/bin/activate"
echo "  pip install -r requirements.txt"
echo ""
echo "Start gunicorn service with:"
echo "sudo systemctl start gunicorn.socket"
echo "sudo systemctl enable gunicorn.socket"

