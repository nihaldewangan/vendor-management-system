from rest_framework import serializers
from .models import Vendor, PurchaseOrder, HistoricalPerformance


class VendorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Vendor
        fields = '__all__'

    def update(self, instance, validated_data):
        # Exclude the field to prevent from being updated
        validated_data.pop('vendor_code', None)
        return super().update(instance, validated_data)


class PurchaseOrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PurchaseOrder
        fields = '__all__'

    def update(self, instance, validated_data):
        # Fields to exclude from being updated
        fields_to_exclude = ['po_number', 'vendor', 'order_date', 'issue_date', 'acknowledgment_date']
        # Remove the excluded fields from validated_data
        for field in fields_to_exclude:
            validated_data.pop(field, None)
        return super().update(instance, validated_data)


class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = HistoricalPerformance
        fields = '__all__'