from django.http import JsonResponse
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated
from .serializer import *


class LoginView(APIView):


    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=400)
        

class vendor_api(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        vendor_serializer = VendorSerializer(data=request.data)
        if vendor_serializer.is_valid():
            vendor_serializer.save()
            return JsonResponse({'status':'success', 'message':'vendor created successfully'})
        else:
            return JsonResponse({'status':'failed', 'message':vendor_serializer.errors}, status=400)
        
    def get(self, request, vendor_id=None):
        if vendor_id:
            try:
                vendor_obj = Vendor.objects.select_related().get(pk=vendor_id)
                vendor_serializer = VendorSerializer(vendor_obj)
            except Exception as e:
                return JsonResponse({ 'status':'failed', 'data':f'{e}' }, status=400)
        else:
            vendor_qs = Vendor.objects.all()
            vendor_serializer = VendorSerializer(vendor_qs, many=True)

        return JsonResponse({ 'status':'success', 'data':vendor_serializer.data })
    
    def put(self, request, vendor_id=None):
        if vendor_id:
            try:
                vendor_obj = Vendor.objects.select_related().get(pk=vendor_id)
                vendor_serializer = VendorSerializer(vendor_obj, data=request.data, partial=True)
                if vendor_serializer.is_valid():
                    vendor_serializer.save()
                    return JsonResponse({ 'status':'success', 'data':vendor_serializer.data }, status=201)
                else:
                    return JsonResponse({ 'status':'failed', 'data':vendor_serializer.errors }, status=400)
            except Exception as e:
                return JsonResponse({ 'status':'failed', 'data':f'{e}' }, status=400)

        else: 
            return JsonResponse({ 'status':'failed', 'data':'vendor id missing' }, status=400)
        
    def delete(self, request, vendor_id=None):
        if vendor_id:
            try:
                vendor_obj = Vendor.objects.get(pk=vendor_id)
                vendor_obj.delete()
                return JsonResponse({ 'status':'success', 'data':'vendor deleted' })
            except Exception as e:
                return JsonResponse({ 'status':'failed', 'data':f'{e}' }, status=400)
        else: 
            return JsonResponse({ 'status':'failed', 'data':'vendor id missing' }, status=400)


class purchase_order_api(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        purchase_order_serializer = PurchaseOrderSerializer(data=request.data)
        if purchase_order_serializer.is_valid():
            purchase_order_serializer.save()
            return JsonResponse({'status':'success', 'message':'PurchaseOrder created successfully'})
        else:
            return JsonResponse({'status':'failed', 'message':purchase_order_serializer.errors}, status=400)
        
    def get(self, request, po_id=None):
        if po_id:
            try:
                purchase_order_obj = PurchaseOrder.objects.select_related().get(pk=po_id)
                purchase_order_serializer = PurchaseOrderSerializer(purchase_order_obj)
            except Exception as e:
                return JsonResponse({ 'status':'failed', 'data':f'{e}' }, status=400)
        else:
            PurchaseOrder_qs = PurchaseOrder.objects.all()
            purchase_order_serializer = PurchaseOrderSerializer(PurchaseOrder_qs, many=True)

        return JsonResponse({ 'status':'success', 'data':purchase_order_serializer.data })
    
    def put(self, request, po_id=None):
        if po_id:
            try:
                purchase_order_obj = PurchaseOrder.objects.select_related().get(pk=po_id)
                purchase_order_serializer = PurchaseOrderSerializer(purchase_order_obj, data=request.data, partial=True)
                if purchase_order_serializer.is_valid():
                    purchase_order_serializer.save()
                    return JsonResponse({ 'status':'success', 'data':purchase_order_serializer.data }, status=201)
                else:
                    return JsonResponse({ 'status':'failed', 'data':purchase_order_serializer.errors }, status=400)
            except Exception as e:
                return JsonResponse({ 'status':'failed', 'data':f'{e}' }, status=400)

        else: 
            return JsonResponse({ 'status':'failed', 'data':'PurchaseOrder id missing' }, status=400)
        
    def delete(self, request, po_id=None):
        if po_id:
            try:
                purchase_order_obj = PurchaseOrder.objects.get(pk=po_id)
                purchase_order_obj.delete()
                return JsonResponse({ 'status':'success', 'data':'PurchaseOrder deleted' })
            except Exception as e:
                return JsonResponse({ 'status':'failed', 'data':f'{e}' }, status=400)
        else: 
            return JsonResponse({ 'status':'failed', 'data':'PurchaseOrder id missing' }, status=400)


class vendor_performance_api(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, vendor_id=None):
        if vendor_id:
            try:
                historical_performance_obj = HistoricalPerformance.objects.get(vendor=vendor_id)
                historical_performance_serializer = HistoricalPerformanceSerializer(historical_performance_obj)
                return JsonResponse({ 'status':'success', 'data':historical_performance_serializer.data })
            except Exception as e:
                return JsonResponse({ 'status':'failed', 'data':f'{e}' }, status=400)
        else:
            JsonResponse({ 'status':'failed', 'data':'vendor id missing' }, status=400)


class vendor_acknowledge_api(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, po_id=None):
        if po_id:
            purchase_order_qs = PurchaseOrder.objects.filter(pk=po_id)
            if purchase_order_qs.exists():
                purchase_order_obj = purchase_order_qs.first()
                purchase_order_obj.acknowledgment_date=timezone.now()
                purchase_order_obj.save()
                return JsonResponse({ 'status':'success', 'data':'order has been received' }, status=200)
            else:
                return JsonResponse({ 'status':'failed', 'data':'invalid purchase order id' }, status=400)
        else:
            return JsonResponse({ 'status':'failed', 'data':'PurchaseOrder id missing' })
