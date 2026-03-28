# Module 11 Project — Production Observability Stack

## Goal

Deploy a production-ready system with:
- CloudWatch dashboards for metrics
- Cost tracking and alarms
- Error handling and logging
- Multi-region failover
- Rate limiting

## Implementation

### Step 1: Enable Bedrock Logging

```python
bedrock = boto3.client('bedrock')

bedrock.put_model_invocation_logging_configuration(
    loggingConfig={
        'cloudWatchConfig': {
            'logGroupName': '/aws/bedrock/invocations',
            'roleArn': 'arn:aws:iam::...:role/BedrockLoggingRole'
        }
    }
)
```

### Step 2: Create CloudWatch Alarms

```python
cloudwatch = boto3.client('cloudwatch')

cloudwatch.put_metric_alarm(
    AlarmName='bedrock-error-rate',
    MetricName='InvokeModel.SystemErrors',
    Namespace='AWS/Bedrock',
    Statistic='Sum',
    Period=300,
    Threshold=10,
    AlarmActions=['arn:aws:sns:us-east-1:...:alert-topic']
)
```

### Step 3: Build Wrapper with Error Handling

```python
def invoke_with_resilience(prompt):
    for attempt in range(3):
        try:
            response = client.converse(
                modelId='...',
                messages=[{'role': 'user', 'content': prompt}]
            )
            return response
        except Exception as e:
            if attempt < 2:
                time.sleep(2 ** attempt)
            else:
                raise
```

### Step 4: Create Dashboard (CDK)

```python
# Use AWS CDK to create dashboard infrastructure
# Shows: latency, errors, token usage, cost
```

## Key Components

- CloudWatch Logs (requests/responses)
- CloudWatch Metrics (latency, errors, costs)
- SNS Alarms (notification on failures)
- Cost analysis (per-model, per-user)
- Dashboard (visual monitoring)
