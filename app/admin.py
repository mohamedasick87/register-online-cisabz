from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ExportMixin
from import_export.widgets import ManyToManyWidget
from .models import Registration, Event

# Custom filter for technical events
class TechnicalEventFilter(admin.SimpleListFilter):
    title = 'Technical Events'
    parameter_name = 'technical_events'

    def lookups(self, request, model_admin):
        # Filter only technical events
        technical_events = Event.objects.filter(event_type='technical')
        return [(event.id, event.name) for event in technical_events]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(technical_events__id=self.value())
        return queryset

# Custom filter for non-technical events
class NonTechnicalEventFilter(admin.SimpleListFilter):
    title = 'Non-Technical Events'
    parameter_name = 'non_technical_events'

    def lookups(self, request, model_admin):
        # Filter only non-technical events
        non_technical_events = Event.objects.filter(event_type='non_technical')
        return [(event.id, event.name) for event in non_technical_events]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(non_technical_events__id=self.value())
        return queryset

# Define the import-export resource for the Registration model
class RegistrationResource(resources.ModelResource):
    # Export technical and non-technical events as comma-separated values
    technical_events = fields.Field(
        column_name='technical_events',
        attribute='technical_events',
        widget=ManyToManyWidget(Event, field='name')
    )
    non_technical_events = fields.Field(
        column_name='non_technical_events',
        attribute='non_technical_events',
        widget=ManyToManyWidget(Event, field='name')
    )

    class Meta:
        model = Registration
        fields = (
            'id', 'member_id', 'name', 'college', 'department', 'phone', 'email', 
            'paper_title', 'paper_abstract', 'technical_events', 'non_technical_events', 
            'payment_link', 'transaction_number'
        )  # Specify the fields you want to include in the export
        export_order = (
            'id', 'member_id', 'name', 'college', 'department', 'phone', 'email', 
            'paper_title', 'paper_abstract', 'technical_events', 'non_technical_events', 
            'payment_link', 'transaction_number'
        )  # Control the order of fields in the export

class RegistrationAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = RegistrationResource
    
    # Specify fields to display in the list view
    list_display = ('name', 'college', 'department', 'email', 'phone')
    
    # Add custom filters for technical and non-technical events
    list_filter = (TechnicalEventFilter, NonTechnicalEventFilter)
    
    # Display fields for better searching
    search_fields = ('name', 'college', 'email')

    # Use filter_horizontal to make selecting many-to-many fields easier in forms
    filter_horizontal = ('technical_events', 'non_technical_events')

# Register the models and the admin classes
admin.site.register(Event)
admin.site.register(Registration, RegistrationAdmin)
