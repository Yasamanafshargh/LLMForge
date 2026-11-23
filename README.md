# LLMForge

**A modular Python framework for LLM data preprocessing, with a
Django-based visual workspace.**

LLMForge is an extensible project for preparing text datasets for Large
Language Model (LLM) workflows. It separates data ingestion, text
normalization, chunking, tokenization, vocabulary management, numerical
encoding, and dataset preparation into reusable components.

The project also includes **LLMForge Studio**, a web-based dashboard for
uploading datasets, configuring preprocessing pipelines, running
experiments, and inspecting real execution results.

> **Project status:** Core preprocessing components and the Django
> Studio are implemented. Model architecture, model training, and text
> generation are future development goals.

------------------------------------------------------------------------

## فارسی

# ال‌ال‌ام‌فورج (LLMForge)

**یک چارچوب ماژولار پایتون برای پیش‌پردازش داده‌های مدل‌های زبانی بزرگ،
همراه با یک محیط بصری مبتنی بر جنگو.**

ال ال ام فورج پروژه‌ای توسعه‌پذیر برای آماده‌سازی مجموعه‌داده‌های متنی در
فرایندهای مرتبط با مدل‌های زبانی بزرگ است. این پروژه مراحل مختلف
آماده‌سازی داده، از جمله دریافت داده، نرمال‌سازی متن، قطعه‌بندی، توکن‌سازی،
مدیریت واژگان، تبدیل توکن‌ها به شناسه‌های عددی و آماده‌سازی مجموعه‌داده را
به اجزای مستقل و قابل استفاده مجدد تقسیم می‌کند.

در کنار هسته اصلی، **ال ال ام فورج استودیو** نیز توسعه داده شده است؛ یک
داشبورد تحت وب مبتنی بر Django که امکان بارگذاری مجموعه‌داده‌ها، اجرای
پایپ‌لاین‌های پیش‌پردازش، مدیریت آزمایش‌ها و مشاهده نتایج واقعی اجرای مراحل
را فراهم می‌کند.

> **وضعیت پروژه:** اجزای اصلی پیش‌پردازش و محیط تحت وب
> > پیاده‌سازی شده‌اند. طراحی معماری مدل، آموزش مدل و تولید متن در برنامه
> توسعه آینده قرار دارند.

------------------------------------------------------------------------

## Table of Contents

-   [Features](#features)
-   [Architecture](#architecture)
-   [Processing Workflow](#processing-workflow)
-   [Supported Input Formats](#supported-input-formats)
-   [Installation](#installation)
-   [Running LLMForge Studio](#running-llmforge-studio)
-   [Running Tests](#running-tests)
-   [Example Pipeline Configuration](#example-pipeline-configuration)
-   [Project Structure](#project-structure)
-   [Design Principles](#design-principles)
-   [Roadmap](#roadmap)
-   [Contributing](#contributing)
-   [License](#license)

## قابلیت‌ها

-   معماری ماژولار و توسعه‌پذیر برای مراحل مختلف پیش‌پردازش متن
-   دریافت داده از فایل‌های TXT، JSON، JSONL و CSV
-   نرمال‌سازی متن فارسی با حفظ نشانه‌گذاری و اطلاعات زبانی مهم
-   پشتیبانی از متن فارسی و انگلیسی در توکن‌سازی پایه
-   قطعه‌بندی متن بر اساس جمله
-   توکن‌سازی پایه و مدیریت واژگان
-   پشتیبانی از توکن‌های ویژه مانند `[PAD]`، `[UNK]`، `[BOS]` و `[EOS]`
-   تبدیل توکن‌ها به شناسه‌های عددی و آماده‌سازی داده‌های توالی
-   پیاده‌سازی پایه الگوریتم Byte Pair Encoding (BPE)
-   ابزار تحلیل واژه‌های توقف (Stop Words) فارسی و انگلیسی
-   ثبت جزئیات اجرای پایپ‌لاین و خروجی هر مرحله
-   داشبورد تحت وب برای مدیریت داده‌ها و اجرای آزمایش‌ها

------------------------------------------------------------------------

## Features

### Core preprocessing

-   Modular processing stages with a shared processing contract.
-   Data ingestion from TXT, JSON, JSONL, and CSV files.
-   Persian text normalization, including Unicode normalization and
    common Arabic/Persian character variants.
-   Basic Persian and English tokenization.
-   Sentence-based text chunking.
-   Vocabulary construction and special-token management.
-   Numerical token encoding.
-   Sequence preparation and padding utilities.
-   A baseline Byte Pair Encoding (BPE) implementation.
-   English and Persian stop-word analysis.

### Pipeline execution and tracing

-   Compose independent stages into reusable pipelines.
-   Execute pipelines on individual documents or batches.
-   Capture stage-level input/output snapshots.
-   Record stage configuration, execution duration, status, and errors.
-   Serialize execution traces for inspection.

### LLMForge Studio

-   Upload and browse datasets.
-   Inspect dataset documents and basic statistics.
-   Analyze stop-word frequencies.
-   Run predefined preprocessing pipelines.
-   Store experiment history and stage execution records.
-   Inspect processed text, tokens, token IDs, and execution durations.

------------------------------------------------------------------------

## Architecture

LLMForge is organized into two main parts:

### 1. LLMForge Core

The Core package contains the reusable preprocessing components. It is
designed to remain independent of the web interface.

Main responsibilities:

-   Document representation
-   Data loaders
-   Processing stages and transforms
-   Pipeline orchestration
-   Text normalization
-   Chunking
-   Tokenization and vocabulary
-   Numerical encoding
-   Dataset utilities
-   Execution tracing

### 2. LLMForge Studio

Studio is a Django application that provides a visual interface to the
Core package.

Main responsibilities:

-   Dataset management
-   Experiment configuration and execution
-   Pipeline execution history
-   Stage-level result inspection
-   Dataset and stop-word analytics

Studio calls the Core package through service-layer components. The
preprocessing logic is not implemented inside Django views.

------------------------------------------------------------------------

## Processing Workflow

A typical preprocessing workflow can contain the following stages:

``` text
Input Dataset
     |
     v
Data Ingestion
     |
     v
Text Normalization
     |
     v
Sentence Chunking
     |
     v
Pre-tokenization / Tokenization
     |
     v
Vocabulary Construction
     |
     v
Numerical Encoding
     |
     v
Dataset Preparation
```

The exact stages depend on the selected pipeline. Not every pipeline
necessarily executes every stage.

### Available Studio pipelines

  -----------------------------------------------------------------------
  Pipeline                            Stages
  ----------------------------------- -----------------------------------
  Persian Normalization               Persian text normalization

  Normalization + Chunking            Normalization, then sentence-based
                                      chunking

  Full Preprocessing                  Normalization, chunking,
                                      tokenization, and numerical
                                      encoding
  -----------------------------------------------------------------------

The full preprocessing pipeline currently builds a vocabulary from the
supplied dataset before encoding its documents. For a machine-learning
evaluation workflow, vocabulary fitting should be performed using
training data only, after splitting the original dataset, to avoid
information leakage.

------------------------------------------------------------------------

## Supported Input Formats

  Format   Description
  -------- --------------------------
  TXT      Plain-text documents
  JSON     Documents stored in JSON
  JSONL    One JSON object per line
  CSV      Tabular text data

The exact fields used by JSON and CSV loaders depend on their loader
configuration.

------------------------------------------------------------------------

## Installation

### Requirements

-   Python 3.13 (the current development environment uses Python 3.13)
-   pip
-   Git

### 1. Clone the repository

``` bash
git clone https://github.com/YOUR_USERNAME/LLMForge.git
cd LLMForge
```

Replace `YOUR_USERNAME` with the GitHub account or organization that
hosts the repository. Adjust the repository name if yours is different.

### 2. Create a virtual environment

**Windows PowerShell**

``` powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

``` bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install the project

From the repository root:

``` bash
python -m pip install --upgrade pip
pip install -e .
```

If the project provides a development requirements file, install it as
well:

``` bash
pip install -r requirements-dev.txt
```

------------------------------------------------------------------------

## Running LLMForge Studio

Studio is located in the `studio/` directory.

From the repository root, activate the virtual environment and run:

``` bash
python studio/manage.py migrate
python studio/manage.py runserver
```

Open the local development address shown by Django in your browser
(normally `http://127.0.0.1:8000/`).

To create an administrator account for the Django admin interface:

``` bash
python studio/manage.py createsuperuser
```

Then open:

``` text
http://127.0.0.1:8000/admin/
```

The dashboard can be used to upload a dataset, select a preprocessing
pipeline, run an experiment, and inspect its results.

------------------------------------------------------------------------

## Running Tests

Run the test suite from the repository root:

``` bash
pytest
```

The project has included unit and integration tests for core processing
components, pipeline execution, tracing, and Studio functionality.

------------------------------------------------------------------------

## Example Pipeline Configuration

The Core package is designed around reusable processing stages. A
pipeline can combine stages into a single execution flow.

A simplified conceptual example:

``` python
from llmforge.core.pipeline import Pipeline
from llmforge.cleaning.persian_stage import PersianNormalizationStage

pipeline = Pipeline([
    PersianNormalizationStage(),
])
```

The Django Studio currently exposes predefined pipeline configurations
through its experiment interface.

------------------------------------------------------------------------

## Project Structure

``` text
LLMForge/
├── src/
│   └── llmforge/
│       ├── core/
│       │   ├── document.py
│       │   ├── stage.py
│       │   ├── transform.py
│       │   ├── pipeline.py
│       │   └── trace.py
│       ├── ingestion/
│       ├── cleaning/
│       ├── chunking/
│       ├── tokenization/
│       ├── encoding/
│       ├── batching/
│       ├── dataset/
│       ├── training/
│       └── stopwords/
│
├── studio/
│   ├── manage.py
│   ├── config/
│   └── dashboard_app/
│       ├── models.py
│       ├── views.py
│       ├── services/
│       ├── templates/
│       └── static/
│
├── tests/
├── pyproject.toml
└── README.md
```

Some modules are under active development. The structure above
highlights the main package areas rather than every individual file.

------------------------------------------------------------------------

## Design Principles

### Modularity

Each processing stage has a focused responsibility and can be composed
with other stages.

### Separation of concerns

Data loading, text processing, pipeline orchestration, and web
presentation are kept separate.

### Traceability

Pipeline execution can capture stage-level inputs, outputs,
configurations, durations, and statuses.

### Language-aware preprocessing

Persian-specific normalization is handled explicitly. The preprocessing
workflow aims to preserve meaningful linguistic information rather than
indiscriminately removing punctuation, stop words, or word-order
information.

### Extensibility

The architecture is intended to support additional tokenizers,
preprocessing stages, dataset utilities, and model-related components.

------------------------------------------------------------------------

## Roadmap

The following items represent planned development and should not be
interpreted as already completed.

-   [ ] Expand language-specific normalization and tokenization.
-   [ ] Extend and evaluate the BPE tokenizer.
-   [ ] Add configurable pre-tokenization strategies.
-   [ ] Improve dataset splitting and vocabulary-fitting workflows.
-   [ ] Add richer batching and PyTorch Dataset integration.
-   [ ] Add more dataset and experiment comparison visualizations.
-   [ ] Develop Transformer model components.
-   [ ] Add model training and evaluation workflows.
-   [ ] Add inference and text generation.
-   [ ] Introduce optional background execution for long-running
    experiments.

------------------------------------------------------------------------

## Contributing

Contributions, bug reports, and suggestions are welcome.

When proposing a new preprocessing component, aim to keep it modular,
testable, and independent of the Django presentation layer.

1.  Fork the repository.
2.  Create a feature branch.
3.  Add or update tests.
4.  Run the test suite.
5.  Submit a pull request describing the change.

------------------------------------------------------------------------

## License

No license has been specified yet. Until a license is added to the
repository, all rights remain with the copyright holder. If you intend
the project to be open source, add an appropriate `LICENSE` file.

------------------------------------------------------------------------

## فارسی --- راهنمای پروژه

### ساختار کلی

LLMForge از دو بخش اصلی تشکیل شده است:

**۱. هسته اصلی (Core)**

هسته اصلی شامل اجزای مستقل پردازش متن است. این بخش مسئول نمایش اسناد،
دریافت داده، نرمال‌سازی، قطعه‌بندی، توکن‌سازی، مدیریت واژگان، کدگذاری عددی
و اجرای پایپ‌لاین‌ها است. هسته اصلی به رابط وب وابستگی ندارد و می‌تواند
به‌صورت مستقل استفاده شود.

**۲. محیط بصری LLMForge Studio**

این بخش با استفاده از Django پیاده‌سازی شده و یک رابط تحت وب برای تعامل
با هسته اصلی فراهم می‌کند. کاربران می‌توانند مجموعه‌داده‌ها را بارگذاری
کنند، پایپ‌لاین‌های آماده را اجرا کنند، آزمایش‌ها را مشاهده کنند و خروجی
مراحل مختلف پردازش را بررسی کنند.

### گردش کار پردازش

یک گردش کار معمول در LLMForge می‌تواند شامل مراحل زیر باشد:

1.  دریافت مجموعه‌داده
2.  نرمال‌سازی متن
3.  قطعه‌بندی متن بر اساس جمله
4.  پیش‌توکن‌سازی و توکن‌سازی
5.  ساخت واژگان
6.  تبدیل توکن‌ها به شناسه‌های عددی
7.  آماده‌سازی داده برای مراحل بعدی یادگیری ماشین

با توجه به نوع پایپ‌لاین انتخاب‌شده، ممکن است همه این مراحل اجرا نشوند.

### اصول طراحی

-   **ماژولار بودن:** هر مرحله وظیفه مشخصی دارد و می‌تواند مستقل از سایر
    مراحل توسعه داده شود.
-   **جداسازی مسئولیت‌ها:** دریافت داده، پردازش متن، مدیریت اجرای
    پایپ‌لاین و نمایش نتایج از یکدیگر جدا هستند.
-   **قابلیت ردیابی:** اطلاعات ورودی و خروجی هر مرحله، تنظیمات، مدت زمان
    اجرا و وضعیت پردازش قابل ثبت و بررسی است.
-   **توجه به ویژگی‌های زبان:** در پردازش فارسی تلاش می‌شود اطلاعات زبانی
    مهم، نیم‌فاصله و نشانه‌گذاری بدون حذف غیرضروری حفظ شوند.
-   **توسعه‌پذیری:** معماری پروژه برای اضافه کردن روش‌های جدید توکن‌سازی،
    مراحل پردازش و اجزای مرتبط با مدل‌های زبانی طراحی شده است.

### وضعیت توسعه

در نسخه فعلی، بخش‌هایی از دریافت داده، نرمال‌سازی فارسی، قطعه‌بندی جمله‌ای،
توکن‌سازی پایه، مدیریت واژگان، کدگذاری عددی، تحلیل واژه‌های توقف، اجرای
پایپ‌لاین و ثبت نتایج در محیط Studio پیاده‌سازی شده‌اند.

توسعه معماری Transformer، آموزش مدل، ارزیابی مدل و تولید متن از اهداف
مراحل بعدی پروژه هستند.

------------------------------------------------------------------------

**LLMForge --- From raw text to structured language-model data.**

**LLMForge --- از متن خام تا داده ساخت‌یافته برای مدل‌های زبانی.**
