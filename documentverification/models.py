from django.db import models

class UploadedDocument(models.Model):
    STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Verified', 'Verified'),
    ('Failed', 'Failed'),
    ]
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_type = models.CharField(max_length=150)
    ip_address = models.GenericIPAddressField()
    device_info = models.TextField()
    status = models.CharField(default="Pending", max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.file.name} - {self.status}"
    
    class Meta:
        db_table = 'uploaded_document'


class ExtractedData(models.Model):
    document = models.OneToOneField(UploadedDocument, on_delete=models.CASCADE)
    raw_text = models.TextField()
    name = models.CharField(max_length=100, null=True, blank=True)
    dob = models.CharField(max_length=20, null=True, blank=True)
    doc_number = models.CharField(max_length=50, null=True, blank=True)
    expiry_date = models.CharField(max_length=20, null=True, blank=True)
    llm_verdict = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Extracted Data for {self.document.file.name}"
    class Meta:
        db_table = 'extracted_data'


