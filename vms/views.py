from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from drf_spectacular.utils import extend_schema
from .filters import *
from .models import *
from .permissions import *
from .serializers import *


class VendorViewsSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):

    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            if self.action == "me":
                return [IsVendor()]
            return [IsAuthenticated()]
        elif self.request.method == "PUT":
            if self.action == "me":
                return [IsVendor()]

    @extend_schema(description="Returns the list of Vendors. *Allowed Users*: [`Admin`, `Vendor`, `Purchaser`]", summary="Get vendors list")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(description="Returns the specific Vendor details. *Allowed Users*: [`Admin`, `Vendor`, `Purchaser`]", summary="Retrive vendor details")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(description="Returns Vendor profile details. *Allowed Users*: [`Vendor`]", summary="Retrive my detials", methods=["GET"])
    @extend_schema(description="Updates Vendor details. *Allowed Users*: [`Vendor`]", summary="Update my detials", methods=["PUT"])
    @action(detail=False, methods=["GET", "PUT", "OPTIONS", "HEAD"])
    def me(self, request: Request):
        vendor = get_object_or_404(
            Vendor.objects.all(), user_id=request.user.id)
        if request.method == "GET":
            serializer = VendorSerializer(vendor)
            return Response(serializer.data)
        elif request.method == "PUT":
            serializer = VendorSerializer(vendor, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    @extend_schema(description="Returns Vendor performance matrix. *Allowed Users*: [`Admin`, `Purchaser`, `Vendor`]", summary="Retrive performance matrix")
    @action(detail=True, methods=SAFE_METHODS)
    def performance(self, request: Request, pk: str):
        vendor = get_object_or_404(
            Vendor.objects.all(), pk=pk)
        serializer = VendorPermormanceSerializer(vendor)
        return Response(serializer.data)


class PurchaserViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    serializer_class = PurchaserSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            if self.action == "me":
                return [IsPurchaser()]
            return [IsAdminOrVendor()]
        elif self.request.method == "PUT":
            if self.action == "me":
                return [IsPurchaser()]

    def get_queryset(self):
        queryset = Purchaser.objects.all()
        user = self.request.user
        if user.account_type == "V":
            queryset = queryset.filter(
                orders__vendor__user_id=user.pk).distinct()
        return queryset

    @extend_schema(description="Returns the list of Purchasers based on `Permissions`. *Allowed Users*: [`Admin`, `Vendor`]", summary="Get purchasers list")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(description="Returns the Specific Purchaser details based on `Permissions`. *Allowed Users*: [`Admin`, `Vendor`]", summary="Retrive purchaser details")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(description="Returns Purchaser profile details. *Allowed Users*: [`Purchaser`]", summary="Retrive my detials", methods=["GET"])
    @extend_schema(description="Updates Purchaser details. *Allowed Users*: [`Purchaser`]", summary="Update my detials", methods=["PUT"])
    @action(detail=False, methods=["GET", "PUT", "OPTIONS", "HEAD"])
    def me(self, request: Request):

        purchaser = get_object_or_404(
            Purchaser.objects.all(), user_id=request.user.id)
        if request.method == "GET":
            serializer = PurchaserSerializer(purchaser)
            return Response(serializer.data)
        elif request.method == "PUT":
            serializer = PurchaserSerializer(purchaser, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class PurchaseOrderViewSet(ModelViewSet):
    http_method_names = ("get", "post", "put", "delete", "head", "options")

    @property
    def filterset_class(self):
        if self.request.user.account_type == "P":
            return VendorFilter
        elif self.request.user.account_type == "V":
            return PurchaserFilter

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreatePurchaseOrderSerializer
        elif self.request.method == "GET":
            if self.request.user.account_type == "V":
                return VendorPurchaseOrderSerializer
            elif self.request.user.account_type == "P":
                return PurchaserPurchaseOrderSerializer
            elif self.request.user.is_staff:
                return AdminPurchaseOrderSerializer
        elif self.request.method == "PUT":
            if self.action == "acknowledge":
                return VendorAcknowledgePurchaseOrderSerializer
            if self.action == "delivery":
                return VendorDeliveryPurchaseOrderSerializer
            elif self.action == "rating":
                return QualityRatingPurchaseOrderSerializer
        return CreatePurchaseOrderSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            if self.action == "rating":
                return [IsPurchaser()]
            elif self.action == "acknowledge":
                return [IsVendor()]
            return [IsAuthenticated()]
        elif self.request.method == "POST":
            return [IsPurchaser()]
        elif self.request.method == "PUT":
            if self.action in ["acknowledge", "delivery"]:
                return [IsVendor()]
            elif self.action == "rating":
                return [IsPurchaser()]
            return [IsPurchaser()]
        elif self.request.method == "DELETE":
            return [IsPurchaser()]

    def get_queryset(self):
        queryset = PurchaseOrder.objects.all()
        user = self.request.user

        if user.account_type == "V":
            queryset = queryset.filter(vendor__user_id=user.pk)
        elif user.account_type == "P":
            queryset = queryset.filter(purchaser__user_id=user.pk)
        return queryset

    def get_serializer_context(self):
        try:
            purchaser = Purchaser.objects.get(user_id=self.request.user.pk)
        except Purchaser.DoesNotExist:
            purchaser = None
        return {"purchaser": purchaser}

    @extend_schema(description="Returns the list of `POs` based on `Permissions`. *Allowed Users*: [`Admin`, `Vendor`, `Purchaser`]", summary="List the `PO`s", responses=AdminPurchaseOrderSerializer)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(description="Takes `Vendor ID` and `PO Items` and Returns created `PO ID`. *Allowed Users*: [`Purchaser`]", summary="Create a new `PO`")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(description="Takes `PO ID` and Returns corresponding `PO detials`. *Allowed Users*: [`Admin`, `Vendor`, `Purchaser`]", summary="Retrive the `PO` details")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(description="Takes `PO ID`, `Vendor ID` and `PO Items` and Returns updated `PO`. *Allowed Users*: [`Purchaser`]", summary="Update the existing `PO`")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(description="Takes `PO ID` and perform cancelling and Returns confirmation message. *Allowed Users*: [`Purchaser`]", summary="Cancel the existing `PO`")
    def destroy(self, request: Request, *args, **kwargs):
        purchase_order = self.get_object()
        if purchase_order.acknowledged_date and purchase_order.actual_delivered_date:
            return Response({"message": "Purchase order cannot be cancelled, It seems already delivered"}, status=status.HTTP_400_BAD_REQUEST)
        elif purchase_order.acknowledged_date:
            return Response({"message": "Purchase order cannot be cancelled, It seems it is in transist"}, status=status.HTTP_400_BAD_REQUEST)
        purchase_order.status = "C"
        purchase_order.save()
        return Response({"message": "Puchase Order canceled successfully"}, status=status.HTTP_204_NO_CONTENT)

    @extend_schema(description="Takes `PO ID` and return `Expected Delivery Date` (Utility api for prepopulating `Expected Delivery Date` in DRF Browsable API). *Allowed Users*: [`Vendor`]", methods=["GET"], summary="Utility API for DRF Browsable API")
    @extend_schema(description="Takes `PO ID` and `Expected Delivery Date` and perform acknowdege and Returns confirmation message. *Allowed Users*: [`Vendor`]", methods=["PUT"], summary="Acknowledge the issued `PO`")
    @action(detail=True, methods=["GET", "PUT", "OPTIONS", "HEAD"])
    def acknowledge(self, request: Request, pk):
        purchase_order = self.get_object()

        if request.method == "GET":
            serializer = VendorAcknowledgePurchaseOrderSerializer(
                purchase_order)
            return Response(serializer.data)

        elif request.method == "PUT":
            if purchase_order.acknowledged_date:
                return Response({"message": "This Purchase Order seems acknowledged already."}, status=status.HTTP_400_BAD_REQUEST)
            elif purchase_order.status != "P":
                return Response({"message": "This Purchase Order either cancelled or Delivered already."}, status=status.HTTP_400_BAD_REQUEST)

            serializer = VendorAcknowledgePurchaseOrderSerializer(
                instance=purchase_order,
                data=request.data,
            )
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Purchase Order acknowledged successfully"})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(description="Takes `PO ID` and perform delivery and Returns confirmation message. *Allowed Users*: [`Vendor`]", summary="Deliver the issued `PO`")
    @action(detail=True, methods=["PUT", "OPTIONS", "HEAD"])
    def delivery(self, request: Request, pk: str):
        purchase_order = self.get_object()

        if not purchase_order.acknowledged_date:
            return Response({"message": "Please acknowledge the Purchase Order before delivering"}, status=status.HTTP_400_BAD_REQUEST)
        elif purchase_order.status in ["C", "D"]:
            return Response({"message": "This Purchase Order either cancelled or Delivered already."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = VendorDeliveryPurchaseOrderSerializer(
            instance=purchase_order,
            data=request.data,
        )
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Purchase Order delivered successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(description="Takes `PO ID` and return `Quality Rating` (Utility api for prepopulating `Quality Rating` in DRF Browsable API). *Allowed Users*: [`Purchaser`]", methods=["GET"], summary="Utility API for DRF Browsable API")
    @extend_schema(description="Takes `PO ID` and `Quality Rating` and perform rating and Returns confirmation message. *Allowed Users*: [`Purchaser`]", methods=["PUT"], summary="Rating the delivered `PO`")
    @action(detail=True, methods=["GET", "PUT", "OPTIONS", "HEAD"])
    def rating(self, request: Request, pk: str):
        purchase_order = self.get_object()

        if request.method == "GET":
            serializer = QualityRatingPurchaseOrderSerializer(purchase_order)
            return Response(serializer.data)

        elif request.method == "PUT":
            if purchase_order.status != "D":
                return Response({"message": "You cannot provide quality rating for this Purchase Order, until it's delivered successfully."}, status=status.HTTP_400_BAD_REQUEST)

            serializer = QualityRatingPurchaseOrderSerializer(
                instance=purchase_order,
                data=request.data,
            )
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Purchase Order rating given successfully"})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
