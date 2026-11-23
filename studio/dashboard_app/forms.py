
from django import forms
from .models import Dataset


class DatasetUploadForm(forms.ModelForm):

    class Meta:
        model = Dataset
        fields = [
            "name",
            "description",
            "file_format",
            "source_file",
        ]

        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "e.g. Persian Research Dataset",
            }),
            "description": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Describe your dataset...",
            }),
            "source_file": forms.ClearableFileInput(attrs={
                "accept": ".txt,.json,.jsonl,.csv",
            }),
        }

    def clean_source_file(self):
        file = self.cleaned_data.get("source_file")

        if not file:
            raise forms.ValidationError("Please upload a dataset file.")

        allowed_extensions = {
            "txt", "json", "jsonl", "csv",
        }

        extension = file.name.rsplit(".", 1)[-1].lower()

        if extension not in allowed_extensions:
            raise forms.ValidationError(
                "Unsupported file format. Use TXT, JSON, JSONL, or CSV."
            )

        return file
class ExperimentRunForm(forms.Form):

    name = forms.CharField(
        max_length=255,
        label="Experiment Name",
        widget=forms.TextInput(attrs={
            "placeholder": "e.g. Persian Text Preprocessing",
        }),
    )

    dataset = forms.ModelChoiceField(
        queryset=Dataset.objects.order_by("-created_at"),
        label="Select Dataset",
        empty_label="Choose a dataset",
    )

    pipeline_type = forms.ChoiceField(
        label="Select Pipeline",
        choices=[
            ("normalization", "Persian Normalization"),
            ("normalization_chunking", "Normalization + Chunking"),
            ("full_preprocessing", "Full Preprocessing"),
        ],
    )

class ExperimentRunForm(forms.Form):

    name = forms.CharField(
        max_length=255,
        label="Experiment Name",
        widget=forms.TextInput(attrs={
            "placeholder": "e.g. Persian Text Preprocessing",
        }),
    )

    dataset = forms.ModelChoiceField(
        queryset=Dataset.objects.order_by("-created_at"),
        label="Select Dataset",
        empty_label="Choose a dataset",
    )

    pipeline_type = forms.ChoiceField(
        label="Select Pipeline",
        choices=[
            ("normalization", "Persian Normalization"),
            ("normalization_chunking", "Normalization + Chunking"),
            ("full_preprocessing", "Full Preprocessing"),
        ],
    )