from __future__ import print_function
from crhelper import CfnResource
import logging
import boto3

logger = logging.getLogger(__name__)

helper = CfnResource(json_logging=False, log_level='DEBUG', boto_level='CRITICAL', sleep_on_delete=120, ssl_verify=None)

try:
    route53 = boto3.client('route53')
    pass
except Exception as e:
    helper.init_failure(e)

@helper.delete
def delete(event, context):
    hosted_zone_id = event['ResourceProperties']['HostedZoneId']

    # Get all record sets
    record_sets = route53.list_resource_record_sets(HostedZoneId=hosted_zone_id)['ResourceRecordSets']

    # Delete all non-NS and non-SOA records
    for record in record_sets:
        if record['Type'] not in ['NS', 'SOA']:
            route53.change_resource_record_sets(
                HostedZoneId=hosted_zone_id,
                ChangeBatch={
                    'Changes': [{
                        'Action': 'DELETE',
                        'ResourceRecordSet': record
                    }]
                }
            )


def handler(event, context):
    helper(event, context)
