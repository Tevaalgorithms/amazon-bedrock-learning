# Module 07 — Guardrails

## What Are Guardrails?

**Guardrails** enforce safety policies on model input and output, protecting against harmful content, PII leakage, and off-topic requests.

## Guardrail Configuration

```python
bedrock_client = boto3.client('bedrock')

guardrail = bedrock_client.create_guardrail(
    name='customer-support-guardrail',
    description='Protects customer support interactions',
    contentPolicyConfig={
        'filtersConfig': [
            {
                'type': 'SEXUAL',
                'action': 'BLOCK'
            },
            {
                'type': 'VIOLENCE',
                'action': 'BLOCK'
            },
            {
                'type': 'HATE',
                'action': 'BLOCK'
            }
        ]
    },
    sensitiveInformationPolicyConfig={
        'piiEntitiesConfig': [
            {
                'type': 'EMAIL_ADDRESS',
                'action': 'BLOCK'
            },
            {
                'type': 'CREDIT_CARD',
                'action': 'ANONYMIZE'
            }
        ]
    },
    topicPolicyConfig={
        'topicsConfig': [
            {
                'name': 'cryptography',
                'description': 'Crypto/blockchain',
                'examples': ['bitcoin', 'ethereum'],
                'type': 'DENY'
            }
        ]
    }
)

guardrail_id = guardrail['guardrailId']
```

## Filter Types

| Type | Examples | Action |
|------|----------|--------|
| SEXUAL | Adult content, explicit material | BLOCK |
| VIOLENCE | Harm, weapons, harm instructions | BLOCK |
| HATE | Hate speech, discrimination | BLOCK |
| INSULTS | Rude, disrespectful language | BLOCK |
| MISCONDUCT | Illegal activity, exploitation | BLOCK |

## PII Detection

Automatically detect and handle personal data:

```python
piiEntitiesConfig=[
    {'type': 'EMAIL_ADDRESS', 'action': 'BLOCK'},
    {'type': 'PHONE_NUMBER', 'action': 'BLOCK'},
    {'type': 'NAME', 'action': 'ANONYMIZE'},  # Replace with [NAME]
    {'type': 'CREDIT_CARD', 'action': 'ANONYMIZE'},
    {'type': 'IP_ADDRESS', 'action': 'BLOCK'},
    {'type': 'AWS_ACCOUNT_ID', 'action': 'BLOCK'},
    {'type': 'SECRET_KEY', 'action': 'BLOCK'}
]
```

## Topic Denial

Block off-topic requests:

```python
topicPolicyConfig={
    'topicsConfig': [
        {
            'name': 'hacking',
            'description': 'Hacking and cyber attacks',
            'examples': ['how to hack a website', 'SQL injection tutorial'],
            'type': 'DENY'
        },
        {
            'name': 'medical-advice',
            'description': 'Medical/health diagnosis',
            'examples': ['Do I have cancer?', 'Treat my infection'],
            'type': 'DENY'
        }
    ]
}
```

## Using Guardrails with Models

```python
bedrock_runtime = boto3.client('bedrock-runtime')

response = bedrock_runtime.converse(
    modelId='anthropic.claude-3-5-sonnet-20241022-v1:0',
    messages=[{'role': 'user', 'content': 'Help me...'}],
    guardrailConfig={
        'guardrailIdentifier': 'gr-123',
        'guardrailVersion': 'DRAFT'  # or version number
    }
)
```

## Guardrail Violation Handling

```python
response = bedrock_runtime.converse(...)

if response.get('guardrailAction') == 'BLOCKED':
    violations = response['guardrailAssessment']['contentPolicy']
    for violation in violations:
        print(f"Blocked: {violation['type']}")

    # Handle appropriately
    return "I can't help with that request"
```

## Word Filters

Custom word filtering:

```python
wordPolicyConfig={
    'wordsConfig': [
        {
            'text': 'competitor-name',
            'action': 'BLOCK'
        },
        {
            'text': 'banned-product',
            'action': 'BLOCK'
        }
    ]
}
```

## Grounding Checks

Verify response accuracy against sources:

```python
groundingPolicyConfig={
    'groundingEnabled': True,
    'groundingThreshold': 0.7  # Require 70% confidence
}
```

## Best Practices

1. **Be permissive, not restrictive** — overly strict guardrails frustrate users
2. **Test thoroughly** — false positives harm UX
3. **Monitor violations** — log to detect patterns
4. **Update periodically** — new types of attacks emerge
5. **Combine with context** — guardrails + domain training = better results

## Costs

- Per invocation with guardrails: Standard model cost + guardrail processing
- Overhead minimal (~5% additional cost)

## Gotchas

### 1. Over-Blocking
If guardrail is too strict, legitimate requests get blocked.

### 2. Language Assumptions
PII detection works better in English. Test in your language.

### 3. Logging
Guardrail violations aren't logged by default. Set up CloudWatch logging.

## Next Steps

Module 07 project: Safe pipeline with PII masking and blocked content logging.

## Resources

- **Guardrails Docs:** https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html
- **PII Types:** https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-pii.html
