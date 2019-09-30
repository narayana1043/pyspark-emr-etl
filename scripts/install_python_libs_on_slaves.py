# Install Python libraries on running cluster nodes
from boto3 import client
from sys import argv
import time

try:
    region_name = argv[1]
    clusterId = argv[2]
    script = argv[3]
    print(region_name, clusterId, script)
except:
    print("Syntax: librariesSsm.py [ClusterId] [S3_Script_Path]")
    import sys

    sys.exit(1)

emrclient = client('emr', region_name=region_name)

# Get list of core nodes
instances = emrclient.list_instances(ClusterId=clusterId, InstanceGroupTypes=['CORE'])['Instances']
instance_list = [x['Ec2InstanceId'] for x in instances]
# instance_list = ['i-0af2ba68e81c65cd0', 'i-0257eb07bfe99790d', 'i-0aecb77402c59e68b', 'i-086fb10d2c3bdf4a1']
print('Instance list: ', instance_list)

# Attach tag to core nodes
ec2client = client('ec2', region_name=region_name)
ec2client.create_tags(Resources=instance_list, Tags=[{"Key": "environment", "Value": "coreNodeLibs"}])

ssmclient = client('ssm', region_name=region_name)

# Download shell script from S3
command = "aws s3 cp " + script + " /home/hadoop"
try:
    # TODO modify the code and make it simple and understanble remove the whiles if possible and use a funtion
    first_command_status = 'Pending'
    second_command_status = "Pending"
    change_permissions_cmd_status = 'Pending'

    """
    The instance IDs where the command should run. You can specify a maximum of 50 IDs. If you prefer not to list 
    individual instance IDs, you can instead send commands to a fleet of instances using the Targets parameter, which 
    ccepts EC2 tags. 
    """
    first_command = ssmclient.send_command(InstanceIds=instance_list,
                                           DocumentName='AWS-RunShellScript',
                                           Parameters={"commands": [command]})['Command']['CommandId']

    # first_command = ssmclient.send_command(Targets=[{"Key": "tag:environment", "Values": ["coreNodeLibs"]}],
    #                                        DocumentName='AWS-RunShellScript',
    #                                        Parameters={"commands": [command]})['Command']['CommandId']

    while first_command_status in ['Pending', 'InProgress']:

        first_command_progress = ssmclient.list_commands(
            CommandId=first_command,
            Filters=[
                {
                    'key': 'Status',
                    'value': 'Success'
                },
                {
                    'key': 'DocumentName',
                    'value': 'AWS-RunShellScript'
                },
                {
                    'key': 'ExecutionStage',
                    'value': 'Complete'
                },
            ],
        )

        if len(first_command_progress['Commands']) > 0:
            first_command_status = first_command_progress['Commands'][0]['Status']
            print(first_command_progress)

        time.sleep(5)

    change_permissions_cmd = ssmclient.send_command(InstanceIds=instance_list,
                                                DocumentName='AWS-RunShellScript',
                                                Parameters={"commands": ["chmod u+x /home/hadoop/bootstrap.sh"]}
                                                )['Command']['CommandId']

    while change_permissions_cmd_status in ['Pending', 'InProgress']:

        change_permissions_cmd_progress = ssmclient.list_commands(
            CommandId=change_permissions_cmd,
            Filters=[
                {
                    'key': 'Status',
                    'value': 'Success'
                },
                {
                    'key': 'DocumentName',
                    'value': 'AWS-RunShellScript'
                },
                {
                    'key': 'ExecutionStage',
                    'value': 'Complete'
                },
            ],
        )

        if len(change_permissions_cmd_progress['Commands']) > 0:
            change_permissions_cmd_status = change_permissions_cmd_progress['Commands'][0]['Status']
            print(change_permissions_cmd_progress)

        time.sleep(5)

    # Only execute second command if first command is successful
    if first_command_status == 'Success':
        # Run shell script to install libraries

        second_command = ssmclient.send_command(InstanceIds=instance_list,
                                                DocumentName='AWS-RunShellScript',
                                                Parameters={"commands": ["bash /home/hadoop/bootstrap.sh"]},
                                                )['Command']['CommandId']

        while second_command_status in ['Pending', 'InProgress']:
            second_command_progress = ssmclient.list_commands(
                CommandId=second_command,
                Filters=[
                    {
                        'key': 'Status',
                        'value': 'Success'
                    },
                    {
                        'key': 'DocumentName',
                        'value': 'AWS-RunShellScript'
                    },
                    {
                        'key': 'ExecutionStage',
                        'value': 'Complete'
                    },
                ],
            )

            if len(second_command_progress['Commands']) > 0:
                second_command_status = second_command_progress['Commands'][0]['Status']
                print(second_command_progress)

            time.sleep(5)

        print("First command: " + first_command + ": " + first_command_status)
        print("Second command:" + second_command + ": " + second_command_status)

except Exception as e:
    print(e)
