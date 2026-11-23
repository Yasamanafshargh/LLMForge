
document.addEventListener("DOMContentLoaded", () => {

    const stages = {
        ingestion: {
            title: "Data Ingestion",
            description: "Load raw data sources and convert them into standardized Document objects.",
            status: "IMPLEMENTED",
            module: "llmforge.ingestion",
            responsibilities: [
                "Read text files and structured datasets.",
                "Support TXT, JSON, JSONL and CSV formats.",
                "Validate records and text fields.",
                "Preserve source information in document metadata."
            ],
            config: [
                ["Supported formats", "TXT, JSON, JSONL, CSV"],
                ["Output", "List[Document]"],
                ["Text validation", "Enabled"]
            ],
            inputLabel: "RAW DATA",
            outputLabel: "DOCUMENT OBJECTS",
            input: {
                "source": "sample.txt",
                "format": "txt",
                "content": "سلام دنیا. این یک متن نمونه است."
            },
            output: {
                "id": "document_001",
                "text": "سلام دنیا. این یک متن نمونه است.",
                "metadata": {
                    "source": "sample.txt",
                    "format": "txt"
                }
            }
        },

        normalization: {
            title: "Text Normalization",
            description: "Normalize Unicode and Persian-specific character variations while preserving linguistic information.",
            status: "IMPLEMENTED",
            module: "llmforge.cleaning",
            responsibilities: [
                "Apply Unicode NFC normalization.",
                "Standardize Arabic Yeh and Kaf characters.",
                "Optionally convert Arabic-Indic digits.",
                "Normalize repeated whitespace.",
                "Preserve punctuation and ZWNJ characters."
            ],
            config: [
                ["Unicode normalization", "NFC"],
                ["Persian character mapping", "Enabled"],
                ["Digit conversion", "Configurable"],
                ["Whitespace normalization", "Enabled"]
            ],
            inputLabel: "ORIGINAL TEXT",
            outputLabel: "NORMALIZED TEXT",
            input: {
                "text": "مي‌روم   به مدرسه"
            },
            output: {
                "text": "می‌روم به مدرسه",
                "changes": [
                    "Arabic Yeh replaced",
                    "Whitespace normalized"
                ]
            }
        },

        chunking: {
            title: "Text Chunking",
            description: "Divide long documents into smaller text units while preserving document relationships and metadata.",
            status: "IMPLEMENTED",
            module: "llmforge.chunking",
            responsibilities: [
                "Split documents using sentence boundaries.",
                "Group sentences into configurable chunks.",
                "Generate unique IDs for each chunk.",
                "Preserve parent document information.",
                "Keep the original document unchanged."
            ],
            config: [
                ["Chunking strategy", "Sentence-based"],
                ["Sentences per chunk", "Configurable"],
                ["Output", "List[Document]"],
                ["Parent ID tracking", "Enabled"]
            ],
            inputLabel: "DOCUMENT",
            outputLabel: "DOCUMENT CHUNKS",
            input: {
                "id": "document_001",
                "text": "سلام دنیا. این جمله دوم است. این جمله سوم است."
            },
            output: {
                "chunks": [
                    {
                        "id": "document_001_chunk_0",
                        "text": "سلام دنیا. این جمله دوم است."
                    },
                    {
                        "id": "document_001_chunk_1",
                        "text": "این جمله سوم است."
                    }
                ]
            }
        },

        tokenization: {
            title: "Tokenization",
            description: "Convert text into smaller linguistic or subword units using the selected tokenizer.",
            status: "IMPLEMENTED",
            module: "llmforge.tokenization",
            responsibilities: [
                "Support whitespace-based tokenization.",
                "Separate punctuation with BasicTokenizer.",
                "Preserve Persian and English text.",
                "Support ZWNJ within Persian words.",
                "Provide an educational custom BPE implementation."
            ],
            config: [
                ["Available tokenizers", "Whitespace, Basic, BPE"],
                ["Language support", "Persian and English"],
                ["Punctuation handling", "Configurable"],
                ["BPE merges", "Learned from training corpus"]
            ],
            inputLabel: "NORMALIZED TEXT",
            outputLabel: "TOKENS",
            input: {
                "text": "سلام دنیا!"
            },
            output: {
                "tokens": [
                    "سلام",
                    "دنیا",
                    "!"
                ]
            }
        },

        encoding: {
            title: "Numerical Encoding",
            description: "Map tokens to numerical IDs using a vocabulary so that they can be consumed by machine learning models.",
            status: "IMPLEMENTED",
            module: "llmforge.encoding",
            responsibilities: [
                "Map tokens to vocabulary IDs.",
                "Handle unknown tokens.",
                "Optionally add BOS and EOS special tokens.",
                "Store tokens and token IDs in the Document."
            ],
            config: [
                ["Vocabulary", "Required"],
                ["Unknown token", "[UNK]"],
                ["BOS / EOS", "Configurable"],
                ["Output", "List[int]"]
            ],
            inputLabel: "TOKENS",
            outputLabel: "TOKEN IDS",
            input: {
                "tokens": ["سلام", "دنیا", "!"]
            },
            output: {
                "token_ids": [12, 35, 8]
            }
        },

        batching: {
            title: "Batching and Padding",
            description: "Prepare variable-length encoded sequences for batch processing by padding them to a common length.",
            status: "IMPLEMENTED",
            module: "llmforge.batching",
            responsibilities: [
                "Group multiple documents into a batch.",
                "Apply dynamic right-padding.",
                "Generate attention masks.",
                "Use ignore_index for padded target positions.",
                "Support configurable padding values."
            ],
            config: [
                ["Padding strategy", "Right padding"],
                ["Padding ID", "Configurable"],
                ["Target ignore index", "-100"],
                ["Attention mask", "Generated"]
            ],
            inputLabel: "ENCODED SEQUENCES",
            outputLabel: "PADDED BATCH",
            input: {
                "sequence_1": [12, 35, 8],
                "sequence_2": [17, 22]
            },
            output: {
                "input_ids": [
                    [12, 35, 8],
                    [17, 22, 0]
                ],
                "attention_mask": [
                    [1, 1, 1],
                    [1, 1, 0]
                ]
            }
        },

        dataset: {
            title: "Dataset Preparation",
            description: "Organize documents into training, validation and test subsets for downstream machine learning tasks.",
            status: "IMPLEMENTED",
            module: "llmforge.dataset",
            responsibilities: [
                "Split documents into train, validation and test sets.",
                "Configure split ratios.",
                "Support reproducible shuffling with a random seed.",
                "Validate document IDs and split ratios."
            ],
            config: [
                ["Default train ratio", "0.8"],
                ["Default validation ratio", "0.1"],
                ["Default test ratio", "0.1"],
                ["Random seed", "42"]
            ],
            inputLabel: "DOCUMENT COLLECTION",
            outputLabel: "DATASET SPLITS",
            input: {
                "documents": [
                    "document_001",
                    "document_002",
                    "document_003",
                    "document_004",
                    "document_005"
                ],
                "shuffle": true,
                "seed": 42
            },
            output: {
                "train": ["document_003", "document_001", "document_004", "document_002"],
                "validation": [],
                "test": ["document_005"]
            }
        }
    };


    const title = document.getElementById("stage-title");
    const description = document.getElementById("stage-description");
    const status = document.querySelector(".stage-status");
    const moduleName = document.getElementById("stage-module");
    const responsibilities = document.getElementById("stage-responsibilities");
    const config = document.getElementById("stage-config");
    const input = document.getElementById("stage-input");
    const output = document.getElementById("stage-output");

    const inputLabel = document.querySelector(
        ".transformation-grid .code-panel-heading > span"
    );

    const outputLabel = document.querySelectorAll(
        ".transformation-grid .code-panel-heading > span"
    )[1];


    function selectStage(stageName) {

        const stage = stages[stageName];

        if (!stage) {
            return;
        }

        title.textContent = stage.title;
        description.textContent = stage.description;
        status.textContent = stage.status;
        moduleName.textContent = stage.module;

        // Update responsibilities
        responsibilities.replaceChildren();

        stage.responsibilities.forEach(item => {
            const li = document.createElement("li");
            li.textContent = item;
            responsibilities.appendChild(li);
        });

        // Update configuration
        config.replaceChildren();

        stage.config.forEach(([name, value]) => {
            const row = document.createElement("div");
            row.className = "config-row";

            const label = document.createElement("span");
            label.textContent = name;

            const setting = document.createElement("strong");
            setting.textContent = value;

            row.append(label, setting);
            config.appendChild(row);
        });

        // Update input and output examples
        input.textContent = JSON.stringify(stage.input, null, 2);
        output.textContent = JSON.stringify(stage.output, null, 2);

        inputLabel.textContent = stage.inputLabel;
        outputLabel.textContent = stage.outputLabel;

        // Update selected stage appearance
        document.querySelectorAll(".explorer-stage").forEach(button => {
            button.classList.toggle(
                "active",
                button.dataset.stage === stageName
            );
        });
    }


    // Attach click events
    document.querySelectorAll(".explorer-stage").forEach(button => {
        button.addEventListener("click", () => {
            selectStage(button.dataset.stage);
        });
    });

});
