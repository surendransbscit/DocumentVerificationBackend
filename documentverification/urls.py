from django.urls import path
from .views import DocumentUploadView, DocumentListView, DocumentDownloadView,DocumentDeleteView,getDocumentFullDetailsView



urlpatterns = [
    path('upload/', DocumentUploadView.as_view(), name='upload'),
    path('documentslist/', DocumentListView.as_view(), name='list'),
    path('download/<int:pk>/', DocumentDownloadView.as_view(), name='document-download'),
    path('delete/<int:pk>/', DocumentDeleteView.as_view(), name='document-delete'),
    path('details/<int:pk>/', getDocumentFullDetailsView.as_view(), name='document-details'),
]
