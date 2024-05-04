from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils import timezone
from .models import *
from django.db.models import Count, Case, When, IntegerField, Sum, FloatField, F, ExpressionWrapper, DurationField, Avg


@receiver(post_save, sender=PurchaseOrder) 
def populate_on_time_delivery_rate(sender, instance, created, **kwargs):
    if instance.status == 'completed':
        result = PurchaseOrder.objects.filter(vendor=instance.vendor).aggregate(
            completed_before_date=Count(
                Case(
                    When(status='completed', delivery_date__gte=timezone.now(), then=1),
                    output_field=IntegerField(),
                )
            ),
            total_completed=Count(
                Case(
                    When(status='completed', then=1),
                    output_field=IntegerField(),
                )
            ),
            completed_with_rating=Count(
                Case(
                    When(status='completed', quality_rating__isnull=False, then=1),
                    output_field=IntegerField(),
                )
            ),
            total_quality_rating=Sum(
                 Case(
                    When(status='completed', quality_rating__isnull=False, then='quality_rating'),
                    output_field=FloatField(),
                )
            ),
            total_order=Count('id')
        )
        if result['total_completed'] > 0:
            on_time_delivery_rate =  result['completed_before_date']/result['total_completed']
            quality_rating_avg = (result['total_quality_rating']/result['completed_with_rating']) if result['completed_with_rating'] else 0
            fulfillment_rate = result['total_completed']/result['total_order']
            
            historical_performance_qs = HistoricalPerformance.objects.filter(vendor=instance.vendor).update(on_time_delivery_rate=on_time_delivery_rate, quality_rating_avg=quality_rating_avg, fulfillment_rate=fulfillment_rate)
            return historical_performance_qs
    else:
        return 0
  

@receiver(post_save, sender=PurchaseOrder,)
def average_response_time(sender, instance, created, **kwargs):
    if instance.acknowledgment_date:
        response_time = ExpressionWrapper(
            F('acknowledgment_date') - F('issue_date'),
            output_field=DurationField()
        )
        average_response_time = PurchaseOrder.objects.filter(vendor=instance.vendor).values('vendor').annotate(
        avg_response_time=Avg(response_time)
        )
        total_avg_response_seconds = average_response_time[0]['avg_response_time'].total_seconds()
        historical_performance_qs = HistoricalPerformance.objects.filter(vendor=instance.vendor).update(average_response_time=total_avg_response_seconds)
        return historical_performance_qs
    else:
        return 0
    

@receiver(post_save, sender=Vendor)
def create_performace_table(sender, instance, created, **kwargs):
    if created:
        HistoricalPerformance.objects.create(vendor=instance)
        return 1
    return 0
 