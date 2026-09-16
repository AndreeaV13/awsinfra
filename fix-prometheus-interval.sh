#!/bin/bash
ssh -i ~/.ssh/frankfurt.pem ec2-user@52.59.99.130 "sudo sed -i 's/scrape_interval: 15s/scrape_interval: 5s/' /etc/prometheus/prometheus.yml && sudo systemctl restart prometheus && sleep 1 && sudo systemctl is-active prometheus && cat /etc/prometheus/prometheus.yml"
