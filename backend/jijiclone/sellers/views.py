from sellers.models import Seller, Buyer, Item
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .helpers.response import sendRes, sendError
from .serializers import SellerSerializer, ItemSerializer, LoginSerializer
from rest_framework.authtoken.models import Token
from rest_framework import permissions, exceptions, status
import jwt, datetime


class IsJWTAuthenticated(permissions.BasePermission):
    message = {"error": "You are unauthorized to access this resource"}
    
    def has_permission(self, request, view):
        token = request.META['HTTP_AUTHORIZATION'].split()[1]
        try:
            decoded = jwt.decode(token, 'MySecretKey', algorithms='HS256')
        except:
            raise exceptions.PermissionDenied(detail=self.message)
        

        return str(view.email) == decoded['email']



@api_view(['POST'])
@permission_classes((AllowAny,))
def SignUp(request):
    serializer = SellerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        # Encode the email as jwt
        token = jwt.encode({'email': serializer.data['email']}, 'MySecretKey', {'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24) }, algorithm='HS256')
        return sendRes({"user": serializer.data, "token": token}, status_code=201, custom_msg="Sign up successful!")
    return sendError(403, serializer.errors)

@api_view(['POST'])
@permission_classes((AllowAny,))
def LoginView(request):

    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        # Encode the email as jwt
        token = jwt.encode({'email': serializer.validated_data['email']}, 'MySecretKey', {'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24) }, algorithm='HS256')
        return sendRes({"user": serializer.validated_data, "token": token}, status_code=200, custom_msg="Login successful!")
    return sendError(403, serializer.errors)
        

# Get all items of a particular seller and also create new items
class ItemsView(APIView):

    permission_classes = (IsJWTAuthenticated,)
    @property
    def email(self):
        if not hasattr(self, '_email'):
            self._email = Seller.objects.get(pk=self.kwargs['sellerId'])
        return self._email

    def get(self, request, sellerId):
        # items = seller.items.filter(is_sold=False)
        try:
            seller = Seller.objects.get(pk=sellerId)
        except Seller.DoesNotExist:
            return sendError(status_code=404)

        serializer = ItemSerializer(seller.items, many=True)
        return sendRes(data=serializer.data)

    def post(self, request, sellerId):
        serializer = ItemSerializer(data=request.data, context={'pk': sellerId})
        if serializer.is_valid():
            serializer.save()
            # seller.items.add(serializer.data)
            return sendRes(serializer.validated_data, 201, "Item added successfully")
        return sendError(400, serializer.errors)
    

class SingleItemView(APIView):
    permission_classes = (IsJWTAuthenticated,)

    @property
    def email(self):
        if not hasattr(self, '_email'):
            self._email = Seller.objects.get(pk=self.kwargs['sellerId'])
        return self._email

    def get_object(self, sellerId, slug):
        try:
            seller = Seller.objects.get(pk=sellerId)
            
            try:
                item = seller.items.get(slug=slug)
                return item
            except ObjectDoesNotExist:
                return sendError(status_code=404)

        except Seller.DoesNotExist or ObjectDoesNotExist:
            return sendError(status_code=404)  


    def get(self, request, sellerId, slug):
        item = self.get_object(sellerId, slug)
        serializer = ItemSerializer(item)
        return sendRes(data=serializer.data)

    def put(self, request, sellerId, slug):
        item = self.get_object(sellerId, slug)
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return sendRes(data=serializer.validated_data)
        return sendError(400, serializer.errors)

    def patch(self, request, sellerId, slug):
        item = self.get_object(sellerId, slug)
        serializer = ItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return sendRes(data=serializer.validated_data)
        return sendError(400, serializer.errors)

    def delete(self, request, sellerId, slug):
        item = self.get_object(sellerId, slug)
        item.delete()
        return sendRes(None,204,"Item removed successfully!")

@api_view(['GET'])
@permission_classes((AllowAny,))
def GetAllItems(request):

    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        # Encode the email as jwt
        token = jwt.encode({'email': serializer.validated_data['email']}, 'MySecretKey', {'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24) }, algorithm='HS256')
        return sendRes({"user": serializer.validated_data, "token": token}, status_code=200, custom_msg="Login successful!")
    return sendError(403, serializer.errors)

class GetAllItems(APIView):
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination

    def get(self, request):
        
        items = Item.objects.filter(is_sold=0)
        serializer = ItemSerializer(items, many=True)
        
        return sendRes(data=serializer.data)

        