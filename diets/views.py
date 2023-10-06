from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from datetime import datetime
from . import serializers
from .models import DietList, SelectedDiet

class DietView(APIView):
    def get(self, request):
        specific_date = request.query_params.get("created_date", "")
        diets = DietList.objects.filter(user=request.user, created_date=specific_date)
        serializer = serializers.DietSerializer(diets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = serializers.DietSerializer(data=request.data)
        if serializer.is_valid():
            if DietList.objects.filter(user=request.user, created_date=datetime.now(), meal_category=request.data["meal_category"]).exists():
                return Response({'errors':"님 오늘 이미 그거 먹었음"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                if request.data["selected_diet"]:
                    diet = serializer.save(user=request.user)
                    selected_diets_data = request.data.get("selected_diet", [])
                    for selected_diet_data in selected_diets_data:
                        selected_serializer = serializers.SelectedDietSerializer(data=selected_diet_data)
                        if selected_serializer.is_valid():
                            selectedDiet, created = SelectedDiet.objects.get_or_create(
                                food_name=selected_diet_data["food_name"],
                                defaults={
                                    "food_calorie": selected_diet_data["food_calorie"],
                                    "food_gram": selected_diet_data["food_gram"],
                                },
                            )
                            diet.selected_diet.add(selectedDiet.id)  # manytomany field는 add/remove
                        else:
                            return Response(selected_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response({"errors": "음식을 선택하지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PutDiet(APIView):
    def get(self, request, pk):
        try:
            diet = DietList.objects.get(pk=pk)
            serializer = serializers.DietSerializer(diet)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except diet.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    # 한줄 평가 입력
    def put(self, request, pk):
        diet = DietList.objects.get(pk=pk)
        serializer = serializers.DietSerializer(
            diet,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_diet = serializer.save()
            return Response(
                serializers.DietSerializer(updated_diet).data,
                status=status.HTTP_202_ACCEPTED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        diets = DietList.objects.get(pk=pk)
        diets.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
