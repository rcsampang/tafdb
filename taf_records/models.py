from django.db import models
from django.conf import settings

class ConsortiumMember(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Expert(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    expertise = models.TextField(blank=True, null=True)
    consortium_member = models.ForeignKey(ConsortiumMember, null=True, blank=True, on_delete=models.SET_NULL, related_name='experts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class TAFRecord(models.Model):
    SCOPE_CHOICES = [
        ('regional', 'Regional'),
        ('national', 'National'),
        ('City/Municipal', 'City/Municipal'),
        ('site-level', 'Site-level'),
    ]
    COUNTRY_CHOICES = [
        ('Philippines', 'Philippines'),
        ('Indonesia', 'Indonesia'),
        ('Vietnam', 'Vietnam'),
        ('Mozambique', 'Mozambique'),
        ('Other Countries', 'Other Countries'),
    ]
    TA_TYPE_CHOICES = [
        ('Capacity-building', 'Capacity-building'),
        ('Research', 'Research'),
        ('Policy Support', 'Policy Support'),
        ('Technical Advice', 'Technical Advice'),
        ('Others', 'Others'),
    ]
    THEME_CHOICES = [
        ('Sustainable fisheries', 'Sustainable fisheries'),
        ('Sustainable Aquaculture', 'Sustainable Aquaculture'),
        ('Critical Marine Habitats', 'Critical Marine Habitats'),
        ('Blue Economy', 'Blue Economy'),
        ('Livelihoods', 'Livelihoods'),
        ('GEDSI', 'GEDSI'),
        ('Climate Change Adaptation', 'Climate Change Adaptation'),
        ('Others', 'Others'),
    ]

    title = models.CharField(max_length=500)
    country = models.CharField(max_length=100, choices=COUNTRY_CHOICES)
    area = models.CharField(max_length=255, blank=True, null=True) # Province/Region
    scope = models.CharField(max_length=50, choices=SCOPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True, null=True) # Specific location if applicable

    type_of_ta = models.CharField(max_length=100, choices=TA_TYPE_CHOICES)
    type_of_ta_other_details = models.TextField(blank=True, null=True)

    # For themes, using a text field to store multiple themes as a comma-separated string or JSON
    # A ManyToManyField to a Theme model would be more robust if themes are predefined and managed.
    # For simplicity based on current HTML (multi-select), storing as text for now.
    themes_text = models.TextField(blank=True, null=True, help_text='Comma-separated list of themes')

    theme_other_details = models.TextField(blank=True, null=True)

    experts_involved_flag = models.BooleanField(default=False, verbose_name='Experts/Institutions Involved?')
    # Storing expert details as text for now as per plan. Could be a M2M to Expert model.
    experts_details_text = models.TextField(blank=True, null=True, verbose_name='Details of Experts/Institutions')

    remarks = models.TextField(blank=True, null=True)

    # Link to actual Expert models (optional, if we want structured expert linking)
    assigned_experts = models.ManyToManyField(Expert, blank=True, related_name='taf_records')

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='created_taf_records')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    # Consider adding properties to parse/set themes_text as a list
    @property
    def themes_list(self):
        if self.themes_text:
            return [theme.strip() for theme in self.themes_text.split(',')]
        return []

    @themes_list.setter
    def themes_list(self, value_list):
        self.themes_text = ', '.join(value_list)
