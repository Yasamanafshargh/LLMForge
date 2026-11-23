from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .services.dataset_service import DatasetService
from .forms import DatasetUploadForm
from .models import Dataset
from llmforge.stopwords import StopWordAnalyzer
import json
from .forms import ExperimentRunForm
from .services.pipeline_service import PipelineService
from llmforge.core.document import Document
from dashboard_app.services.pipeline_factory import PipelineFactory
from collections import Counter
from dashboard_app.models import Experiment
import traceback

def dashboard(request):
    return render(request, "dashboard_app/dashboard.html")


def dataset_list(request):
    datasets = Dataset.objects.order_by("-created_at")

    return render(
        request,
        "dashboard_app/dataset_list.html",
        {"datasets": datasets},
    )

def dataset_detail(request, dataset_id):
    dataset = get_object_or_404(Dataset, id=dataset_id)

    documents = DatasetService().load(dataset)

    if dataset.document_count != len(documents):
        dataset.document_count = len(documents)
        dataset.save(update_fields=["document_count"])

    analyzer = StopWordAnalyzer()

    document_results = []

    for document in documents:
        result = analyzer.analyze(document.text)

        document_results.append({
            "document": document,
            "analysis": result,
            "frequencies": sorted(
                result.frequencies.items(),
                key=lambda item: (-item[1], item[0]),
            ),
        })

    # Dataset-level statistics
    total_tokens = sum(
        item["analysis"].total_tokens
        for item in document_results
    )

    # Dataset-wide stop word frequencies
    dataset_frequencies = Counter()

    for item in document_results:
        dataset_frequencies.update(
            item["analysis"].frequencies
        )

    top_stop_words = dataset_frequencies.most_common(10)

    total_stop_words = sum(
        item["analysis"].stop_word_count
        for item in document_results
    )

    stop_word_percentage = (
        (total_stop_words / total_tokens) * 100
        if total_tokens > 0
        else 0.0
    )

    return render(
        request,
        "dashboard_app/dataset_detail.html",
        {
            "dataset": dataset,
            "document_results": document_results,
            "total_tokens": total_tokens,
            "total_stop_words": total_stop_words,
            "stop_word_percentage": round(stop_word_percentage, 2),
            "top_stop_words": top_stop_words,
        },
    )
def pipeline_explorer(request):
    print("PIPELINE VIEW METHOD:", request.method)
    print("PIPELINE POST DATA:", request.POST.dict())

    context = {
        "input_text": "",
        "normalized_text": None,
        "trace_json": None,
        "execution_time": None,
        "execution_status": None,
    }

    if request.method == "POST":
        input_text = request.POST.get("input_text", "").strip()
        context["input_text"] = input_text

        if not input_text:
            messages.error(request, "Please enter some text to normalize.")
        else:
            try:
                document = Document(
                    id="normalization_demo",
                    text=input_text,
                    metadata={},
                )

                pipeline = PipelineFactory.create("normalization")

                processed_documents, trace = pipeline.run_with_trace(document)
                normalizer = pipeline.stages[0].normalizer

                _, normalization_steps = normalizer.normalize_with_steps(
                    input_text
                )

                stage = pipeline.stages[0]
                normalizer = stage.normalizer

                normalization_config = {
                    "Unicode Normalization (NFC)": normalizer.normalize_unicode,
                    "Arabic Yeh → Persian Yeh": normalizer.normalize_yeh,
                    "Arabic Kaf → Persian Kaf": normalizer.normalize_kaf,
                    "Arabic Digits → Persian Digits": normalizer.normalize_digits,
                    "Whitespace Normalization": normalizer.normalize_whitespace,
                }

                context.update({
                    "normalized_text": processed_documents[0].text,
                    "trace_json": json.dumps(
                        trace.to_dict(),
                        ensure_ascii=False,
                        indent=2,
                        default=str,
                    ),
                    "execution_time": round(trace.total_duration_ms, 4),
                    "execution_status": "Completed",
                    "normalization_config": normalization_config,
                    "normalization_steps": normalization_steps,
                })

            except Exception as exc:
                print("NORMALIZATION ERROR:", type(exc).__name__, str(exc))

                messages.error(
                    request,
                    f"Normalization failed: {exc}",
                )
    return render(
        request,
        "dashboard_app/pipeline_explorer.html",
        context,
    )

def run_experiment(request):
    if request.method == "POST":
        form = ExperimentRunForm(request.POST)

        if form.is_valid():
            dataset = form.cleaned_data["dataset"]
            pipeline_type = form.cleaned_data["pipeline_type"]
            experiment_name = form.cleaned_data["name"]

            try:
                # Load dataset documents
                documents = DatasetService().load(dataset)

                if not documents:
                    raise ValueError("The selected dataset contains no documents.")

                # Update document count
                if dataset.document_count != len(documents):
                    dataset.document_count = len(documents)
                    dataset.save(update_fields=["document_count"])

                # Create and execute pipeline
                pipeline = PipelineFactory.create(
                    pipeline_type,
                    documents=documents,
                )
                result = PipelineService().execute(
                    pipeline=pipeline,
                    documents=documents,
                    dataset=dataset,
                    experiment_name=experiment_name,
                )

                messages.success(
                    request,
                    f"Experiment '{experiment_name}' completed successfully."
                )

                return redirect(
                    "experiment_history"
                )

            except Exception as exc:
                print("\n========== EXPERIMENT EXECUTION ERROR ==========")
                traceback.print_exc()
                print("================================================\n")

                messages.error(
                    request,
                    f"Experiment execution failed: {exc}"
                )

    else:
        form = ExperimentRunForm()

    return render(
        request,
        "dashboard_app/run_experiment.html",
        {"form": form},
    )

def experiment_history(request):
    experiments = (
        Experiment.objects
        .select_related("dataset")
        .order_by("-created_at")
    )

    return render(
        request,
        "dashboard_app/experiment_history.html",
        {
            "experiments": experiments,
        },
    )
def experiment_detail(request, experiment_id):
    experiment = get_object_or_404(
        Experiment,
        id=experiment_id,
    )

    stage_executions = experiment.stage_executions.all()

    return render(
        request,
        "dashboard_app/experiment_detail.html",
        {
            "experiment": experiment,
            "stage_executions": stage_executions,
        },
    )

def dataset_upload(request):

    if request.method == "POST":
        form = DatasetUploadForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():
            dataset = form.save(commit=False)

            dataset_format = dataset.source_file.name.rsplit(
                ".", 1
            )[-1].lower()

            dataset.file_format = dataset_format
            dataset.save()

            messages.success(
                request,
                f"Dataset '{dataset.name}' uploaded successfully."
            )

            return redirect("dataset_upload")

    else:
        form = DatasetUploadForm()

    return render(
        request,
        "dashboard_app/dataset_upload.html",
        {"form": form},
    )
