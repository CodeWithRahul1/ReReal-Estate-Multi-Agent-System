# Real Estate Chatbot API

## Overview
This API allows users to interact with a chatbot that helps them search for real estate properties based on their preferences, such as location, budget, and number of bedrooms/bathrooms. Users can also schedule property visits.

## Features
- Search for properties based on user preferences.
- Filters properties by **city, budget, bedrooms, and bathrooms**.
- Stores **user search history** to provide personalized recommendations.
- Allows users to **schedule a property visit**.
- Uses **LLM (Large Language Model)** to generate natural language responses.

## Tech Stack
- **Backend:** Django, Django REST Framework (DRF)
- **Database:** PostgreSQL / SQLite
- **AI Model:** Open-source LLM (e.g., Llama 2, Groq)

---

## API Endpoints
### **1. Chatbot Query Endpoint**
**URL:** `/api/chatbot-query/`  
**Method:** `POST`

**Request JSON:**
```json
{
  "query": "Show me houses in New York, with 3-bedrooms"
}
```

**Response JSON (Example):**
```json
{
    "response": "🏠 Modern Apartment (ID: 12): 3 beds, 2 baths, $750000 in New York, NY.\n👉 Type 'Book visit 12 on YYYY-MM-DD at HH:MM AM/PM' to schedule a visit.\n\n🏠 Spacious Condo (ID: 18): 3 beds, 2 baths, $820000 in New York, NY.\n👉 Type 'Book visit 18 on YYYY-MM-DD at HH:MM AM/PM' to schedule a visit."
}
```

### **2. Booking Property Visit**
Users can book a visit by sending a message like:
```
Book visit 12 on 2025-04-10 at 10:30 AM
```
This functionality should be implemented in a **separate booking endpoint** (not covered in this README).

---

## Installation & Setup
### **1. Clone the Repository**
```bash
git clone https://github.com/CodeWithRahul1/ReReal-Estate-Multi-Agent-System.git
cd chatbot-real-estate
```

### **2. Create Virtual Environment & Install Dependencies**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use 'venv\Scripts\activate'
pip install -r requirements.txt
```

### **3. Run Migrations**
```bash
python manage.py migrate
```

### **4. Start the Server**
```bash
python manage.py runserver
```

---

## Database Models
### **Property Model**
```python
class Property(models.Model):
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    is_available = models.BooleanField(default=True)
```

### **User Search History Model**
```python
class UserSearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    query = models.TextField()
    city = models.CharField(max_length=255, null=True, blank=True)
    budget = models.IntegerField(null=True, blank=True)
    bedrooms = models.IntegerField(null=True, blank=True)
    bathrooms = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
```

---

## Future Enhancements
- Add **user authentication** for personalized recommendations.
- Implement a **booking confirmation system**.
- Integrate **Google Calendar API** for visit scheduling.
- Use **ElasticSearch** for more efficient property searches.

---

