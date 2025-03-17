from rest_framework import generics
from .models import Property
from .serializers import PropertySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Property
from .serializers import PropertySerializer, BookingSerializer
import joblib
import pandas as pd
import re
from rest_framework.decorators import api_view
from rest_framework.response import Response
import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from langchain_groq import ChatGroq 
# from langchain.llms import Ollama
from django.utils.dateparse import parse_date, parse_time
from langchain_groq import ChatGroq
from .models import Property , UserSearchHistory, Booking
from langchain.schema import AIMessage, HumanMessage
from django.db.models import Q


class PropertyListCreateView(generics.ListCreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

class PropertyRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer


@api_view(['GET'])
def buyer_agent(request):
    """
    Buyer Agent: Filters properties based on user preferences
    """
    budget = request.GET.get('budget', None)
    location = request.GET.get('location', None)
    bedrooms = request.GET.get('bedrooms', None)
    
    properties = Property.objects.all()

    if budget:
        properties = properties.filter(price__lte=budget)  # Less than or equal to budget
    if location:
        properties = properties.filter(location__icontains=location)  # Case-insensitive match
    if bedrooms:
        properties = properties.filter(bedrooms=bedrooms)

    serializer = PropertySerializer(properties, many=True)
    return Response(serializer.data)


# Load trained model
model = joblib.load("price_model.pkl")

@api_view(['POST'])
def predict_price(request):
    """
    Price Prediction Agent: Predicts property price based on input features.
    """
    try:
        data = request.data
        location = data.get("location", "")
        bedrooms = int(data.get("bedrooms", 0))
        bathrooms = int(data.get("bathrooms", 0))
        area_sqft = int(data.get("area_sqft", 0))

        # Convert location to numerical category (Assumption: same order as training)
        location_mapping = {
            "Los Angeles": 0, "New York": 1, "Miami": 2, "Denver": 3, "Chicago": 4,
            "Austin": 5, "San Francisco": 6, "Seattle": 7, "Las Vegas": 8, "Boston": 9
        }
        location_code = location_mapping.get(location, -1)  # Default -1 if location is unknown

        if location_code == -1:
            return Response({"error": "Invalid location"}, status=400)

        # Predict price
        input_data = pd.DataFrame([[location_code, bedrooms, bathrooms, area_sqft]],
                                  columns=["location", "bedrooms", "bathrooms", "area_sqft"])
        predicted_price = model.predict(input_data)[0]

        return Response({"predicted_price": round(predicted_price, 2)})

    except Exception as e:
        return Response({"error": str(e)}, status=400)    


GROQ_API_KEY = "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" # Set in environment variables

# 🟢 Use Ollama (local model) or Groq (cloud-based LLM)
use_ollama = True  # Change to False if you want to use Groq

if use_ollama:    
    if not GROQ_API_KEY:
        raise ValueError("Groq API key is missing! Set GROQ_API_KEY as an environment variable.")
    llm = ChatGroq(model_name="llama-3.1-8b-instant", api_key=GROQ_API_KEY)  # Use Groq

@api_view(['POST'])
def chatbot_query(request):
    """
    Chatbot Agent with Buyer Agent and User History Tracking.
    """
    try:
        user_query = request.data.get("query", "").lower()
        user = request.user if request.user.is_authenticated else None  # Handle authenticated users

        if not user_query:
            return Response({"error": "Query cannot be empty"}, status=400)

        # Extract user preferences from the query
        budget, bedrooms, bathrooms = None, None, None
        city_names = Property.objects.values_list('location', flat=True).distinct()
        city_names = [city.lower() for city in city_names]
        matched_city = next((city for city in city_names if city in user_query), None)

        print("🔍 Matched City:", matched_city)  # Debugging Output

        words = user_query.split()
        for i, word in enumerate(words):
            if word in ["under", "below"] and i + 1 < len(words) and words[i + 1].startswith("$"):
                try:
                    budget = int(words[i + 1].replace("$", "").replace(",", ""))
                except ValueError:
                    pass

        for word in words:
            if "-bedroom" in word:
                bedrooms = int(word.split("-")[0])
            if "-bathroom" in word:
                bathrooms = int(word.split("-")[0])

        # Save user search history
        UserSearchHistory.objects.create(
            user=user, query=user_query, city=matched_city, budget=budget, bedrooms=bedrooms, bathrooms=bathrooms
        )

        # Fetch matching properties
        filters = Q(is_available=True)
        if matched_city:
            filters &= Q(location__iexact=matched_city)  # Use strict city matching
        if budget:
            filters &= Q(price__lte=budget)
        if bedrooms:
            filters &= Q(bedrooms=bedrooms)
        if bathrooms:
            filters &= Q(bathrooms=bathrooms)

        properties = Property.objects.filter(filters).values("id", "title", "location", "price", "bedrooms", "bathrooms")
        property_list = list(properties)

        # **Strictly handle no matching properties**
        if matched_city and not property_list:
            return Response({"response": f"No properties found in {matched_city} based on your criteria."})

        # **Use Search History for Recommendations (if needed)**
        if not property_list and user:
            past_searches = UserSearchHistory.objects.filter(user=user).order_by("-timestamp")[:3]
            if past_searches.exists():
                last_search = past_searches.first()
                filters = Q(location__iexact=last_search.city) if last_search.city else Q()
                properties = Property.objects.filter(filters, is_available=True).values(
                    "id", "title", "location", "price", "bedrooms", "bathrooms"
                )
                property_list = list(properties)

        if not property_list:
            return Response({"response": "No matching properties found based on your preferences."})

        # Format response with booking instructions
        property_info = "\n\n".join([
            f"🏠 {prop['title']} (ID: {prop['id']}): {prop['bedrooms']} beds, {prop['bathrooms']} baths, ${prop['price']} in {prop['location']}."
            f"\n👉 Type 'Book visit {prop['id']} on YYYY-MM-DD at HH:MM AM/PM' to schedule a visit."
            for prop in property_list
        ])

        system_prompt = f"""You are a real estate buyer agent. Based on the user's preferences and past searches, suggest the best property options.

        Available properties:
        {property_info}

        If no perfect match exists, suggest the closest available option.
        """

        ai_response = llm.invoke(system_prompt + "\n\nUser Query: " + user_query)
        response_content = ai_response.content if hasattr(ai_response, "content") else str(ai_response)

        return Response({"response": response_content})

    except Exception as e:
        return Response({"error": str(e)}, status=500)


def handle_booking(user, property_id, visit_date, visit_time):
    """Handles booking requests"""
    if not user:
        return {"error": "You must be logged in to book a visit."}

    # Validate Property
    try:
        property_obj = Property.objects.get(id=property_id, is_available=True)
    except Property.DoesNotExist:
        return {"error": "Property not available"}

    # Check Availability
    if Booking.objects.filter(property=property_obj, visit_date=visit_date, visit_time=visit_time).exists():
        return {"error": "This slot is already booked"}

    # Create Booking
    Booking.objects.create(
        user=user,
        property=property_obj,
        visit_date=visit_date,
        visit_time=visit_time,
        status="Pending"
    )

    return {
        "message": f"Booking confirmed for {property_obj.title} on {visit_date} at {visit_time}.",
        "status": "Pending"
    }

# llm = ChatGroq(model_name="llama-3.1-8b-instant", api_key="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") 