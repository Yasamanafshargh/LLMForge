from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path(
        "pipeline/",
        views.pipeline_explorer,
        name="pipeline_explorer",
    ),
    path(
        "experiments/",
        views.experiment_history,
        name="experiment_history",
    ),
    path(
        "experiments/run/",
        views.run_experiment,
        name="run_experiment",
    ),  
    path(
        "experiments/<int:experiment_id>/",
        views.experiment_detail,
        name="experiment_detail",
    ),
    path(
        "datasets/upload/",
        views.dataset_upload,
        name="dataset_upload",
    ),
    path(
        "datasets/<int:dataset_id>/",
        views.dataset_detail,
        name="dataset_detail",
    ),
    path(
        "datasets/",
        views.dataset_list,
        name="dataset_list",
    ),
]