
This project’s aim is to implement a system that will not only alert the team of issues, but also automate the resolution of these issues on the devices.



In this project, the author’s primary aim, is to try to modernize a legacy solution, where users were responsible to review vast amounts of messages to determine the issue before being tasked with then finding a solution. 

The team aim to employ AWS technologies, that will not only alert them of issues on the network devices, but also correct them, as and when they happen.

The team also aim to create a virtual routing lab using the network software emulator known as “GNS3@. This lab will be accessible over the internet so the team can access and configure them when required.

To assist in achieving automated resolution of issues, the authors also aim to review how to implement the YANG/ Netconf protocols into the solution network. As relatively recent protocols, these may present challenges to configure correctly.

Further to this, where possible, the team also aim to write their own code for the python components in this project. For instance, the syslog server functionality, the Lambda functions and the netconf server will be achieved with python code.



Project Objectives

There are numerous project objectives, and they are listed below. 


•	Build AWS environment for all components of project
•	Build VPC which will house the EC2 instance
•	Build a Linux EC2 Instance which will run the syslog server
•	Create virtual interface on the EC2 instance which will listen for Syslog health messages
•	Configure the on premise server as a GNS3 routing lab server
•	Create the virtual routing environment in GNS3
•	Write Python code which configures the EC2 instance as a syslog server
•	Write Python code which configures the EC2 instance as a Netconf server
•	Configure routers to communicate with one another using OSPF protocol
•	Configure the routers to send syslog event messages to syslog server running as EC2 instance
•	Route these messages to a Kinesis stream and CloudWatch for analytical information
•	Set retention policy in CloudWatch to retain the syslog messages for two weeks.
•	Configure SNS message to alert team on any syslog event from categories 0-3
•	Create lambda function to query Kinesis stream for “neighbour down” messages and alert team of their occurrence 
•	Configuring a Netconf server using Python to resolve issues on routers with API calls utilising the Netconf/YANG protocols 

