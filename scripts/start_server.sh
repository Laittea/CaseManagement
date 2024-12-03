#!/bin/bash
# Start the Apache server
sudo systemctl start apache2

# Enable Apache to start on boot
sudo systemctl enable apache2
