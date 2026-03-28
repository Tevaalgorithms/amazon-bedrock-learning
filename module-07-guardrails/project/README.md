# Module 07 Project — Safe Content Pipeline

## Goal

Build a pipeline that protects against harmful content:
- Detect PII (email, credit card, phone)
- Mask or block detected PII
- Log violations
- Filter hate speech, violence

## Implementation

```python
import boto3

bedrock = boto3.client('bedrock')

# Create guardrail
guardrail = bedrock.create_guardrail(
    name='safe-pipeline',
    contentPolicyConfig={
        'filtersConfig': [
            {'type': 'SEXUAL', 'action': 'BLOCK'},
            {'type': 'VIOLENCE', 'action': 'BLOCK'}
        ]
    },
    sensitiveInformationPolicyConfig={
        'piiEntitiesConfig': [
            {'type': 'EMAIL_ADDRESS', 'action': 'BLOCK'},
            {'type': 'CREDIT_CARD', 'action': 'ANONYMIZE'}
        ]
    }
)

# Use in Converse
response = client.converse(
    modelId='...',
    messages=[...],
    guardrailConfig={'guardrailIdentifier': guardrail['guardrailId']}
)

# Check if blocked
if response.get('guardrailAction') == 'BLOCKED':
    print("Content blocked by guardrail")
```

## Test Cases

- "My email is test@example.com" → Should block
- "My card is 4111-1111-1111-1111" → Should anonymize
- "I hate you" → Depends on configuration
- "Help me hack a website" → Should block (if configured)
