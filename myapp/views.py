from django.core import serializers
from django.http import JsonResponse
from django.db.models import Q

from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from myapp.models import Product, Category
import json


@api_view(['POST'])
def add_product(request):
    '''Create a new Product.

    :param name(required): the name of the product.
    :type name: string
    :param color(required): the color of the product
    :type color: string
    :param image(required): the image need to be used in the product.
    :type image: file
    :param price(required): the price of the product
    :type price: float
    :param category(required): the id of the category that need to be used
    :type category: integer

    :returns: message
    :rtype: dictionary
    '''
    try:
        if request.POST and request.FILES:
            is_error = False
            name = request.data.get('name')
            color = request.data.get('color')
            image = request.data.get('image')
            category_id = request.data.get('category')
            price = request.data.get('price')
            if not name:
                message = 'Name is Mandatory'
                is_error = True
            if not color:
                message = 'Color is Mandatory'
                is_error = True
            if not category_id:
                message = 'Category Id is Mandatory'
                is_error = True
            if not price:
                message = 'Price is Mandatory'
                is_error = True
            if is_error:
                return Response({"error": message}, 
                            status=status.HTTP_400_BAD_REQUEST)
            category = Category.objects.get(id=category_id)
            p = Product(name=name,
                        color=color,
                        image=image,
                        category=category,
                        price=price)
            p.save()

            return Response({"message": 'Product Added Successfully'})
        elif not request.FILES:
            return Response({"error": "Image is Mandatory."}, 
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "All Fields are Mandatory."}, 
                            status=status.HTTP_400_BAD_REQUEST)
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except KeyError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_products(request):
    '''List all Products which are active

    :returns: List of all active Products
    :rtype: dictionary
    '''
    try:
        data = list(Product.objects.filter(is_active=True).values())
        return JsonResponse({'data': data, 'count': len(data)}, safe=False)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_categories(request):
    '''List all Categories which are active

    :returns: List of all active Categories
    :rtype: dictionary
    '''
    try:
        data = list(Category.objects.filter(is_active=True).values())
        return JsonResponse({'data': data, 'count': len(data)}, safe=False)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def filter_products(request):
    '''List all Categories which are active
    
    :param keyword(optional): keyword needed for search.
    :type name: string

    :returns: List of all Matched Products
    :rtype: dictionary
    '''
    keyword = request.data.get('keyword')
    try:
        category = Category.objects.get(category_name__icontains=keyword,
                                        is_active=True)
        data = Product.objects.filter((Q(name__icontains=keyword) |
                                      Q(color__icontains=keyword) |
                                      Q(category=category)) &
                                      Q(is_active=True)).values()
    except Category.DoesNotExist as e:
        data = Product.objects.filter((Q(name__icontains=keyword) |
                                      Q(color__icontains=keyword)) &
                                      Q(is_active=True)).values()
    if len(list(data)) > 0:
        return JsonResponse({'data': list(data), 'count': len(data)},
                             safe=False)
    else:
        return JsonResponse({'message': (f"No Data Found for '{keyword}'"
                             f"keyword")}, safe=False)
