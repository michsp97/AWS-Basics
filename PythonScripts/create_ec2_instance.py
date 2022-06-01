#!/usr/bin/ env python3
# Version 1.0.0
# Date: 05/29/2022
# Author Michelle Sanchez
# Usage python3 ./create_ec2_instance.py --name "Test-instance-1" --key "MyKP-1" --sg "sg-000000000b"

import boto3
import argparse

ec2_client = boto3.client('ec2', region_name="us-east-1")
image_id = 'ami-0022f774911c1d690'  # Newest AMI Amazon Linux image as today


def create_instance(instance_name, key_name=None, security_groups=None):
    """
    This function will create an ec2 instance with basic config and encrypted gp3 volume,
    key name and security group are given to this instance to be able to connect via SSH
    :param instance_name: Name that we would want to give to out instance
    :param key_name: OPTIONAL The Key pair to securely connect to the instance
    :param security_groups: OPTIONAL security groups to attach to your instance
    :return:
    """

    if security_groups is None:
        security_groups = []
    options = {
        "BlockDeviceMappings": [
            {
                'DeviceName': '/dev/xvda',
                'Ebs': {
                    'DeleteOnTermination': True,
                    'VolumeSize': 10,
                    'VolumeType': 'gp3',
                    'Encrypted': True
                }
            }
        ],
        "ImageId": image_id,
        "InstanceType": 't2.micro',
        "MaxCount": 1,
        "MinCount": 1,
        "Monitoring": {
            'Enabled': False
        },
        "SecurityGroupIds": security_groups,
        "DryRun": False,
        "InstanceInitiatedShutdownBehavior": 'stop',
        "TagSpecifications": [
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': instance_name
                    },
                ]
            },
        ]
    }

    if key_name:
        options["KeyName"] = key_name

    ec2_client.run_instances(**options)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create EC2 instance')
    parser.add_argument('--name', type=str, required=True, help="Instance name")
    parser.add_argument('--key', type=str, required=False, help='Key Par value')
    parser.add_argument('--sg', type=str, required=False, help='Security groups attached')
    args = parser.parse_args()

    ec2_name = args.name
    key_par = args.key

    if args.sg:
        sg = [args.sg]
    else:
        sg = []

    create_instance(ec2_name, key_par, sg)
