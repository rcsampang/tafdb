from django.db import models
from django.conf import settings
# from taf_records.models import TAFRecord # This would cause circular import if Template is in taf_records
# from templates.models import Template # This is fine

class Attachment(models.Model):
    # Link to either TAFRecord or Template. GenericForeignKey could be an option too.
    taf_record = models.ForeignKey('taf_records.TAFRecord', null=True, blank=True, on_delete=models.CASCADE, related_name='attachments')
    template_document = models.ForeignKey('templates.Template', null=True, blank=True, on_delete=models.CASCADE, related_name='attachments') # If templates themselves can have attachments (e.g. supporting docs for a template) or if this is the template file itself. The plan says "Template model ... file_path", so Template.file is the main file. This attachment model is more for TAFRecord files.

    # For TAF Record attachments, as per index.html categories
    FILE_CATEGORIES = [
        ('Concept Note', 'Concept Note'),
        ('Terms of Reference', 'Terms of Reference'),
        ('Full Proposal', 'Full Proposal'),
        ('Budget TA Contract', 'Budget TA Contract'),
        ('Deliverables/Milestone Outputs', 'Deliverables/Milestone Outputs'),
        ('Invoices', 'Invoices'),
        ('Proof of Payment', 'Proof of Payment'),
        ('Evaluation Report', 'Evaluation Report'),
        ('References', 'References'),
        ('Other Files', 'Other Files'),
    ]
    category = models.CharField(max_length=100, choices=FILE_CATEGORIES, blank=True, null=True)
    file = models.FileField(upload_to='attachments/%Y/%m/%d/') # Store in MEDIA_ROOT/attachments/YYYY/MM/DD/
    file_name = models.CharField(max_length=255, blank=True, null=True) # Original file name
    description = models.TextField(blank=True, null=True)

    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.file and not self.file_name:
            self.file_name = self.file.name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.file_name or f'Attachment {self.id}'
