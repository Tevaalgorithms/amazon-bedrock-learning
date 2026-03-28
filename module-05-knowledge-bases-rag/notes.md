# Module 05 — Knowledge Bases & RAG

## What is RAG?

**Retrieval-Augmented Generation** — using relevant documents to augment model context, improving accuracy and reducing hallucinations.

## Architecture

```
User Query
    ↓
Embed Query
    ↓
Search Vector Store (OpenSearch Serverless)
    ↓
Retrieve Top K Documents
    ↓
Prompt: "Context: [documents] Question: [query]"
    ↓
Claude Responds (using actual data, not memory)
```

## Why RAG?

- **Accuracy** — model responds based on actual data, not training data
- **Recency** — documents can be updated without retraining
- **Transparency** — can show which documents were used
- **Cost** — avoid fine-tuning

## Bedrock Knowledge Bases

Bedrock provides managed Knowledge Bases that handle:

1. **Document Ingestion** — upload files (PDF, HTML, TXT, DOCX, etc)
2. **Chunking** — split documents into manageable pieces
3. **Embeddings** — convert chunks to vectors using Titan Embeddings
4. **Vector Store** — OpenSearch Serverless (AWS-managed)
5. **Retrieval** — find relevant chunks for a query

### Knowledge Base Setup

1. Create S3 bucket for documents
2. Create OpenSearch Serverless collection
3. Create Knowledge Base (points to S3 + OpenSearch)
4. Upload documents
5. Wait for sync job to complete
6. Query via RetrieveAndGenerate API

## APIs

### RetrieveAndGenerate (Full RAG Pipeline)

```python
response = client.retrieve_and_generate(
    input={'text': 'What is the return policy?'},
    retrieveAndGenerateConfiguration={
        'type': 'KNOWLEDGE_BASE',
        'knowledgeBaseConfiguration': {
            'knowledgeBaseId': 'kb-123',
            'modelArn': 'arn:aws:bedrock:...::foundation-model/anthropic.claude-3-5-haiku-20241022-v1:0',
            'retrievalConfiguration': {
                'vectorSearchConfiguration': {
                    'numberOfResults': 5  # Top 5 chunks
                }
            }
        }
    }
)
```

Returns: (answer, citations)

### Retrieve Only

```python
response = client.retrieve(
    knowledgeBaseId='kb-123',
    retrievalConfiguration={
        'vectorSearchConfiguration': {
            'numberOfResults': 5
        }
    },
    text='What is the return policy?'
)

for result in response['retrievalResults']:
    print(result['content'])  # Document chunk
    print(result['score'])    # Relevance score (0-1)
```

## Chunking Strategies

How to split documents affects retrieval quality:

### Fixed Size
- Split every N tokens
- Simple, fast
- Can cut mid-sentence

### Semantic
- Split where meaning changes
- Better, but slower
- Requires analysis

### By Section
- Use document structure (headings)
- Most accurate for structured docs
- Requires parsing

Bedrock supports default chunking (~300 tokens) or custom.

## Embedding Models

Convert text to vectors for semantic search:

**Titan Embeddings (AWS):**
- 1536 dimensions
- Multilingual
- Low latency
- Cost: $0.10 per 1k input tokens

**Cohere Embeddings:**
- 1024 dimensions
- Also multilingual

Same embedding model for both documents and queries is critical.

## Vector Database: OpenSearch Serverless

AWS-managed vector search:

```python
# Bedrock handles this automatically
# But you can also query directly:

opensearch_client = boto3.client('opensearchserverless')

response = opensearch_client.search(
    index='bedrock-kb-index',
    body={
        'size': 5,
        'query': {
            'knn': {
                'vector_field': {
                    'vector': [0.1, 0.2, ...],  # Query embedding
                    'k': 5
                }
            }
        }
    }
)
```

## Metadata Filtering

Retrieve documents with specific metadata:

```python
response = client.retrieve(
    knowledgeBaseId='kb-123',
    retrievalConfiguration={
        'vectorSearchConfiguration': {
            'numberOfResults': 5,
            'filter': {
                'equals': {
                    'key': 'department',
                    'value': 'finance'
                }
            }
        }
    },
    text='Budget for Q4'
)
```

## Citations & Sources

RAG should show sources:

```python
response = client.retrieve_and_generate(...)

answer = response['output']['text']
sources = response['citations']  # List of used documents

for citation in sources:
    print(f"Source: {citation['generatedResponse']['textSpan']}")
    print(f"Document: {citation['retrievedReferences'][0]['content']['text']}")
```

## Chunking Best Practices

1. **Don't chunk too small** — lose context
2. **Don't chunk too large** — dilute signal
3. **Maintain structure** — keep related info together
4. **Add metadata** — author, date, category
5. **Test retrieval** — verify quality with queries

## Costs

| Component | Cost |
|-----------|------|
| Embeddings (Titan) | $0.10 per 1M tokens |
| OpenSearch Serverless (Retrieval) | $0.03 per retrieval unit/hour (~$0.003 per query) |
| Bedrock (Generation) | Standard model pricing |

Example: 100 queries/day on 100k document KB ≈ $5-10/month

## Gotchas

### 1. Sync Takes Time
After uploading documents, sync can take minutes. Don't query immediately.

### 2. Stale Data
Documents are synced once. Updates require re-upload.

### 3. Chunking Quality
Poor chunking = poor retrieval. Test different chunk sizes.

### 4. Context Window Limits
Even with 200k context, if you retrieve too many chunks, may exceed limit.

### 5. Cost of Irrelevant Retrieval
If retrieval is poor, you'll retrieve garbage docs and waste tokens.

## Next Steps

Module 05 project: Build document Q&A system with PDFs.

## Resources

- **KB Docs:** https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html
- **RAG Patterns:** https://docs.aws.amazon.com/bedrock/latest/userguide/rag-use-case.html
- **OpenSearch Serverless:** https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless.html
