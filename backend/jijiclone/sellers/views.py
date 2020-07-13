from sellers.models import Seller, Buyer, Item
from rest_framework.decorators import api_view
from .helpers.response import sendRes, sendError
from .serializers import SellerSerializer, ItemSerializer


@api_view(['POST'])

def signUp(request):
    serializer = SellerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return sendRes(data=serializer.data, status_code=201, custom_msg="Sign up successful!")
    return sendError(403, serializer.errors)
        

@api_view(['GET','POST'])

# Get all items of a particular seller and also create new items

def itemsView(request, sellerId):
    try:
        seller = Seller.objects.get(pk=sellerId)
    except Seller.DoesNotExist:
        return sendError(status_code=404)

    if request.method == 'GET':
        # items = seller.items.filter(is_sold=False)

        serializer = ItemSerializer(seller.items, many=True)
        return sendRes(data=serializer.data)

    elif request.method == 'POST':
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            seller.items.add(serializer.data)
            return sendRes(serializer.data, 201, "Item added successfully")
        return sendError(400, serializer.errors)
    

# class Items(APIView):

#     def get(self, request, seller_id):
#         seller = Seller.objects.get(pk=seller_id)
#         items = seller.items.filter(is_sold=0)

#         serializer = ItemSerializer(items)
#         return

# Create your views here.
