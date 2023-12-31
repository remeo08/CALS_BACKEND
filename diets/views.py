from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from datetime import datetime
from dateutil.relativedelta import *
from . import serializers
from users.serializers import UserSerializer
from .models import DietList, SelectedDiet, QuantityMultiple
from users.models import User


class DietView(APIView):
    def get(self, request):
        specific_date = request.query_params.get("created_date", "")

        diet_saved_date=DietList.objects.filter(user=request.user).values_list("created_date", flat=True).order_by("created_date").distinct()

        diets = DietList.objects.filter(user=request.user, created_date=specific_date)
        serializer = serializers.DietSerializer(diets, many=True)

        user = User.objects.get(id=request.user.id)
        user_serializer = UserSerializer(user)

        return Response(
            {
                "data": serializer.data,
                "diet_saved_date": diet_saved_date,
                "user_weight": request.user.weight,
                "user_recommended_calorie": user_serializer.data["recommended_calorie"],
            },
            status=status.HTTP_200_OK,
        )
    
    # def get(self, request):
    #     dietlist = DietList.objects.filter(user=request.user)
    #     serializer = serializers.DietSerializer(dietlist, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = serializers.DietSerializer(data=request.data)
        if serializer.is_valid():
            # meal_category 중복 예외처리
            if DietList.objects.filter(
                user=request.user,
                created_date=request.data["created_date"],
                meal_category=request.data["meal_category"],
            ).exists():
                return Response(
                    {"errors": "님 오늘 이미 그거 먹었음"}, status=status.HTTP_400_BAD_REQUEST
                )
            else:
                # selected_diet 빈 배열 예외처리
                if request.data["selected_diet"]:
                    diet_list_instance = serializer.save(user=request.user)
                    selected_diets_data = request.data.get("selected_diet", [])
                    for selected_diet_data in selected_diets_data:
                        selectedDiet, created = SelectedDiet.objects.get_or_create(
                            food_name=selected_diet_data["food_name"],
                            defaults={
                                "food_calorie": selected_diet_data["food_calorie"],
                                "food_gram": selected_diet_data["food_gram"],
                            },
                        )

                        QuantityMultiple.objects.create(
                            diet_list=diet_list_instance,
                            selected_diet=selectedDiet,
                            food_quantity=selected_diet_data["food_quantity"],
                        )
                        # serializer.selected_diet.add(selectedDiet.id)  # manytomany field는 add/remove
                        # diet.selected_diet.add(selectedDiet.id)

                        serializer = serializers.DietSerializer(diet_list_instance)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(
                        {"errors": "음식을 선택하지 않았습니다."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 수량, selected_diet 수정
    def put(self, request):
        created_date = request.query_params.get("created_date", "")
        meal_category = request.query_params.get("meal_category", "")
        diets = DietList.objects.get(
            user=request.user,
            created_date=created_date,
            meal_category=meal_category, 
        )
        diets.meal_calorie=request.data["meal_calorie"]
        diets.save()

        if request.data["modified_diet"]:
            for modified_diet in request.data["modified_diet"]:
                selected_id = SelectedDiet.objects.get(food_name=modified_diet["selected_diet"]["food_name"])
                quantity = diets.quantitymultiple_set.get(selected_diet=selected_id.id)
                quantity.food_quantity = modified_diet["food_quantity"]
                quantity.save()

        if request.data["deleted_diet"]:
            for deleted_diet in request.data["deleted_diet"]:
                selected_id = SelectedDiet.objects.get(food_name=deleted_diet["selected_diet"]["food_name"])
                diets.quantitymultiple_set.get(selected_diet=selected_id.id).delete()

        if request.data["selected_diet"]:
            for selected_diet_data in request.data["selected_diet"]:
                selectedDiet, created = SelectedDiet.objects.get_or_create(
                    food_name=selected_diet_data["selected_diet"]["food_name"],
                    defaults={
                        "food_calorie": selected_diet_data["selected_diet"]["food_calorie"],
                        "food_gram": selected_diet_data["selected_diet"]["food_gram"],
                    },
                )

                QuantityMultiple.objects.create(
                    diet_list=diets,
                    selected_diet=selectedDiet,
                    food_quantity=selected_diet_data["food_quantity"],
                )

        serializer = serializers.DietSerializer(diets)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


    def delete(self, request):
        created_date = request.query_params.get("created_date", "")
        meal_category = request.query_params.get("meal_category", "")
        diets = DietList.objects.get(
            user=request.user, created_date=created_date, meal_category=meal_category
        )
        diets.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewView(APIView):
    def put(self, request):
        created_date = request.query_params.get("created_date", "")
        specific_reviews = DietList.objects.filter(
            created_date=created_date, user=request.user
        )
        for review in specific_reviews:
            review.daily_review = request.data["daily_review"]
            review.save()
        serializer = serializers.ReviewPutSerializer(specific_reviews, many=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)