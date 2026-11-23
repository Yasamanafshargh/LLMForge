from llmforge.ingestion import JSONLLoader
from llmforge.cleaning.persian_stage import PersianNormalizationStage
from llmforge.chunking.sentence_transform import SentenceChunkTransform
from llmforge.tokenization.bpe.bpe_trainer import BPETrainer
from llmforge.tokenization.bpe.bpe_tokenizer import BPETokenizer
from llmforge.tokenization.vocabulary import Vocabulary
from llmforge.encoding import TokenEncodingStage
from llmforge.batching import PaddingStage

DATASET_PATH = "data/raw/persian_experiment.jsonl"

# 1. Load dataset
loader = JSONLLoader()
documents = loader.load(DATASET_PATH)

print(f"Loaded {len(documents)} documents\n")

# 2. Normalize Persian text
normalizer = PersianNormalizationStage()

for document in documents:
    original_text = document.text

    normalizer.process(document)

    print(f"Document ID: {document.id}")
    print(f"Original:   {original_text}")
    print(f"Normalized: {document.text}")
    print("-" * 70)

print("\nNORMALIZATION INTEGRITY CHECK")

for document in documents:
    print(document.id, repr(document.text))
    print("Double spaces:", "  " in document.text)
# 3. Split documents into chunks

chunk_transform = SentenceChunkTransform(
    sentences_per_chunk=2
)

chunked_documents = []

for document in documents:
    chunks = chunk_transform.transform(document)
    chunked_documents.extend(chunks)

print("\nCHUNKING RESULTS")
print("=" * 70)

print("\nCHUNK INTEGRITY CHECK")

for document in chunked_documents:
    print(document.id)
    print(repr(document.text))

for document in chunked_documents:
    print(f"Chunk ID: {document.id}")
    print(f"Parent: {document.metadata['parent_document_id']}")
    print(f"Chunk index: {document.metadata['chunk_index']}")
    print(f"Text: {document.text}")
    print("-" * 70)

# 4. Train BPE tokenizer

corpus = [
    document.text
    for document in chunked_documents
]

trainer = BPETrainer()

merges = trainer.train(
    corpus=corpus,
    num_merges=30
)

print("\nBPE TRAINING RESULTS")
print("=" * 70)

print("Number of merges:", len(merges))

for index, pair in enumerate(merges):
    merged_token = pair[0] + pair[1]

    print(
        f"Merge {index + 1}: "
        f"{pair[0]} + {pair[1]} -> {merged_token}"
    )

# 5. Build BPE model

bpe_model = trainer.build_model()

print("\nBPE MODEL")
print("=" * 70)

print("Vocabulary size:", len(bpe_model.vocabulary))
print("Special tokens:", bpe_model.special_tokens)

print("\nVocabulary:")
print(bpe_model.vocabulary)

# 6. Initialize tokenizer and vocabulary

tokenizer = BPETokenizer.from_model(bpe_model)

vocabulary = Vocabulary(
    special_tokens=bpe_model.special_tokens
)

vocabulary.build(bpe_model.vocabulary)

print("\nVOCABULARY SIZE:", len(vocabulary))


# 7. Tokenize our chunks

print("\nTOKENIZATION RESULTS")
print("=" * 70)

for document in chunked_documents:

    tokens = tokenizer.tokenize(document.text)

    print("Document:", document.id)
    print("Text:", document.text)
    print("Tokens:", tokens)
    print("-" * 70)

# 8. Numerical encoding

encoding_stage = TokenEncodingStage(
    tokenizer=tokenizer,
    vocabulary=vocabulary,
    add_bos=True,
    add_eos=True
)

print("\nNUMERICAL ENCODING")
print("=" * 70)

for document in chunked_documents:

    encoding_stage.process(document)

    print("Document:", document.id)
    print("Tokens:", document.tokens)
    print("Token IDs:", document.token_ids)
    print("Sequence length:", len(document.token_ids))
    print("-" * 70)

# 9. Padding and attention masks

padding_stage = PaddingStage(
    pad_token_id=vocabulary.token_to_id["[PAD]"],
    padding=True
)

padded_documents = padding_stage.process(
    chunked_documents
)

print("\nFINAL MODEL INPUT")
print("=" * 70)

for document in padded_documents:

    print("Document:", document.id)
    print("Token IDs:", document.token_ids)
    print("Attention Mask:", document.metadata["attention_mask"])
    print("Final Length:", len(document.token_ids))
    print("-" * 70)

print("\nFINAL VALIDATION")

for document in padded_documents:
    ids = document.token_ids
    mask = document.metadata["attention_mask"]

    print(f"\nDocument: {document.id}")
    print("Sequence length:", len(ids))
    print("Mask length:", len(mask))
    print("Actual token count:", sum(mask))
    print("Padding count:", mask.count(0))

    assert len(ids) == len(mask)
    assert len(ids) == 75
    assert all(token_id in vocabulary.id_to_token for token_id in ids)
    assert all(
        token_id == vocabulary.token_to_id["[PAD]"]
        for token_id, attention in zip(ids, mask)
        if attention == 0
    )

print("\nAll validation checks passed!")