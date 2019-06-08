import boto3
import os
def get_ec2_con_for_give_region(my_region):
	session = boto3.Session(region_name=my_region)
	ec2_con_re = session.resource(service_name='ec2')
	return ec2_con_re
	
def list_instances_on_my_region(ec2_console):
	for each_instance in ec2_con_re.instances.all():
		print(each_instance.id) 

def get_instances_state(ec2_con_re, instance_id):
	for instance_state in ec2_con_re.instances.filters(Filters=[{'Name': 'instance-id','Values': [instance_id]}]):
		in_state = instance_state.state['Name']
	return in_state

def start_instances(ec2_con_re, instance_id):
	pr_st = get_instances_state(ec2_con_re, instance_id)
	if pr_st == 'running':
		print("Instance is already running")
	else:
		for each in ec2_con_re.instances.filter(Filters=[{'Name': 'instance-id', 'Values':[instance_id]}]):
			each.start()
			print("please wait it is going to start, once if it is started then we will let you know")
			each.wait_until_runnig()
			print("Now it is running")
			
def stop_instances(ec2_con_res, instance_id):
	pr_st = get_instances_state(ec2_con_res, instance_id)
	if pr_st == 'stopped':
		print("Instance is already stopped")
	else:
		for each in ec2_con_res.instances.filter(Filters=[{'Name': 'instance-id', 'Values': [instance_id]}]):
			each.stop()
			print("please wait it is going to stop, once if it is stopped then we will let you know")
			each.wait_until_stopped()
			print("Now it is stopped") 
			
def main():
	my_region = input("Enter your region name: ") 
	print("Please wait...connecting to your AWS EC2 console.....") 
	ec2_console = get_ec2_con_for_give_region(my_region) 
	print("Please wait listing all instances ids in your region {}".format(my_region)) 
	list_instances_on_my_region(ec2_console)
	instance_id = input("Now choose your instance id to start or stop: ") 
	start_stop = input("Enter either start or stop for you EC2 Instance: ") 
	while True: 
		if start_stop not in ['start', 'stop']: 
			start_stop = input("Please Enter only start or stop commands: ")
			continue
		else:
			break 
	if start_stop == 'start':
		start_instances(ec2_console, instance_id)
	elif start_stop == 'stop': 
		stop_instances(ec2_console, instance_id)
		
if _name_ == '__main__': 
	os.system('cls') 
	main()