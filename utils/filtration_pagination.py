from django.core.paginator import Paginator,EmptyPage
from django.db.models import Q
from rest_framework import status

def filtration_processing(filtration_data):
    if filtration_data:
        filters = {}
        q_particulars=[]
        for key,value in filtration_data.items():
            if key == "username" and  value != "":
                filters["username__icontains"] = value
          
            elif key == "created_at" and value != "":
                filters["created_at__date"] = value

            elif key == "name" and value != "":
                filters["name__icontains"] = value
           
        q_object = [Q(**{key:value}) for key,value in filters.items()]

        if len(q_particulars)>0:
           q_object.append(q_particulars)

        return q_object
    
    return []


def pagination_processing(pagination_data,attribute_type):
    limit = 30
    offset = 1
    if pagination_data:
        limit = pagination_data.get("row_count",30)
        offset = pagination_data.get("page",1)
    paginator = Paginator(attribute_type,limit)
    try:
        attribute_type_page = paginator.page(offset)
        return {"data":attribute_type_page,"status":status.HTTP_200_OK}
    except EmptyPage:
        return {"message":"No more pages","status":status.HTTP_404_NOT_FOUND}


