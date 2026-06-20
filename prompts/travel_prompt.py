def create_prompt(data):
    return f"""
You are an AI Travel Planner.

Create a travel plan using these details.

Destination: {data.destination}
Days: {data.days}
Budget: {data.budget}
Travelers: {data.travelers}
Travel Type: {data.travel_type}
Interests: {data.interests}

Include:

1. Day-wise itinerary
2. Places to visit
3. Food recommendations
4. Estimated budget
5. Transportation
6. Packing tips
7. Travel tips

Make the response well formatted.
"""