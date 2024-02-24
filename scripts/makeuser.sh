#!/bin/sh

sudo useradd -m -s "/bin/bash" -G docker cdsrv
sudo passwd cdsrv
su cdsrv
