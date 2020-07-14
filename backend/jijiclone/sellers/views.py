from sellers.models import Seller, Buyer, Item
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from .helpers.response import sendRes, sendError
from .serializers import SellerSerializer, ItemSerializer


@api_view(['POST'])

def SignUp(request):
    serializer = SellerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return sendRes(data=serializer.data, status_code=201, custom_msg="Sign up successful!")
    return sendError(403, serializer.errors)
        

@api_view(['GET','POST'])

# Get all items of a particular seller and also create new items

def ItemsView(request, sellerId):
    try:
        seller = Seller.objects.get(pk=sellerId)
    except Seller.DoesNotExist:
        return sendError(status_code=404)

    if request.method == 'GET':
        # items = seller.items.filter(is_sold=False)

        serializer = ItemSerializer(seller.items, many=True)
        return sendRes(data=serializer.data)

    elif request.method == 'POST':
        serializer = ItemSerializer(data=request.data, context={'pk': sellerId})
        if serializer.is_valid():
            serializer.save()
            # seller.items.add(serializer.data)
            return sendRes(serializer.validated_data, 201, "Item added successfully")
        return sendError(400, serializer.errors)
    
@api_view(['GET','PUT','DELETE'])

def SingleItemView(request, sellerId, slug):
        try:
            seller = Seller.objects.get(pk=sellerId)
            
            try:
                item = seller.items.get(slug=slug)
            except ObjectDoesNotExist:
                return sendError(status_code=404)

        except Seller.DoesNotExist or ObjectDoesNotExist:
            return sendError(status_code=404)   


        if request.method == 'GET':
            serializer = ItemSerializer(item)
            return sendRes(data=serializer.data)

        elif request.method == 'PUT':
            serializer = ItemSerializer(item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return sendRes(data=serializer.validated_data)
            return sendError(400, serializer.errors)

        elif request.method == 'DELETE':
            item.delete()
            return sendRes(None,204,"Item removed successfully!")


# class Items(APIView):

#     def get(self, request, seller_id):
#         seller = Seller.objects.get(pk=seller_id)
#         items = seller.items.filter(is_sold=0)

#         serializer = ItemSerializer(items)
#         return

# Create your views here.
