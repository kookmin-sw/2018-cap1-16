import boto3, time

ec2 = boto3.client('ec2', region_name='us-west-2', aws_access_key_id='AKIAIDEKND2OCPILXFVQ', aws_secret_access_key='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')
data = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])['Reservations']

print(len(data[0]['Instances']))
'''
for instance in data[0]['Instances']:
    print(instance['InstanceId'])
    ec2.start_instances(InstanceIds = [instance['InstanceId']])
'''
#time.sleep(300)
for instance in data[0]['Instances']:
    print(instance['InstanceId'])
    ec2.stop_instances(InstanceIds = [instance['InstanceId']])

#print(ec2.start_instances())
#instances = ec2.instances.filter(
#    Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])

#for status in ec2.meta.client.describe_instance_status()['InstanceStatuses']:
#    print(status)
#
#for instance in instances:
#    print(instance.run_instances())