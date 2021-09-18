#!/bin/bash
USERNAME="{@username}"
IP="{@host}"
PORT="22"
ssh ${USERNAME}@${IP} -${PORT} -t "{cd /your/working/folder/here} ; bash --login"
