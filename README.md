ssl-health
==========

To run the application make use of the following command:
python main.py 

To enable the application, you need to copy the config.example.py to config.py. 

Arguments
-h	Give host to test. Default port is 443. host[:port]
-p	Give a printer to use. Default printer is tui.

Any printers can be added by copying the example.py printer to the required printer

Any test can be edited or added in the tests folder. Copy the example.py and begin programming :)

Updating CA certificates
========================

Don't forget to edit your root certificate location in the config.py. This ensures an updated root certificate check.
