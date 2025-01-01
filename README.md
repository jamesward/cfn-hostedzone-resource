# AWS CloudFormation Hosted Zone Resource

This project provides a custom CloudFormation resource for cleaning up HostedZone records so the HostedZone can be deleted.

> Backstory: If you create a HostedZone and an associated Certificate (using DNS validation) with CloudFormation, the HostedZone can't be deleted because unmanaged records are added to the HostedZone. This makes rollbacks or removals hard.  Adding a CustomResource based on this repo that references the HostedZone enables it to be cleaned up before it is deleted.

When deployed as a Lambda, Domains can be managed as custom resources, like:

```yaml
  HostedZoneManagerFunction:
    Type: AWS::Lambda::Function
    Properties:
      Code:
        S3Bucket:
          Ref: HostedZoneManagerBuildBucket
        S3Key: function.zip
      Handler: index.handler
      Role:
        Fn::GetAtt:
          - HostedZoneManagerRole
          - Arn
      Runtime: python3.9
      Timeout: 10

  foocomHostedZoneCleanup:
    Type: AWS::CloudFormation::CustomResource
    Properties:
      ServiceTimeout: 70
      ServiceToken:
        Fn::GetAtt:
          - HostedZoneManagerFunction
          - Arn
      DomainName: foo.com
      HostedZoneId:
        Ref: foocomHostedZone
```
