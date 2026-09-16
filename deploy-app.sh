#!/bin/bash
ssh -i ~/.ssh/frankfurt.pem ec2-user@52.59.99.130 "cd /var/www/app && sudo git pull && sudo systemctl restart flask && sudo systemctl is-active flask"
