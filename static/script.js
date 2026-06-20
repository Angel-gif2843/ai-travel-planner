document.getElementById("travelForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    const result = document.getElementById("result");
    result.textContent = "Generating travel plan...";

    const data = {
        destination: document.getElementById("destination").value,
        days: parseInt(document.getElementById("days").value),
        budget: document.getElementById("budget").value,
        travelers: parseInt(document.getElementById("travelers").value),
        travel_type: document.getElementById("travel_type").value,
        interests: document.getElementById("interests").value
    };

    try {
        // 1. ADDED: Make the real API network call to your FastAPI backend
        const response = await fetch("http://127.0.0.1:8000/generate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.statusText}`);
        }

        const responseData = await response.json();
        const planData = responseData.plan;

        // 2. Clear the loading text and establish the summary header
        result.innerHTML = `
            <div style="background: #eef2f7; padding: 20px; border-radius: 8px; margin-bottom: 25px; border-left: 5px solid #0056b3; font-family: sans-serif;">
                <h3 style="margin-top:0; color: #0056b3;">Trip Itinerary for ${planData.destination}</h3>
                <p style="margin-bottom:0; color: #333;"><strong>Total Estimated Budget/Cost:</strong> ${planData.total_estimated_cost}</p>
            </div>
            <div id="itinerary-timeline" style="font-family: sans-serif;"></div>
        `;

        const timeline = document.getElementById("itinerary-timeline");

        // 3. Loop through the JSON array and render beautifully styled individual day cards
        planData.itinerary.forEach(item => {
            const dayCard = document.createElement("div");
            dayCard.style.borderLeft = "4px solid #28a745";
            dayCard.style.padding = "15px";
            dayCard.style.marginBottom = "15px";
            dayCard.style.background = "#ffffff";
            dayCard.style.boxShadow = "0 2px 5px rgba(0,0,0,0.05)";
            dayCard.style.borderRadius = "0 6px 6px 0";

            // Map activities array to clean HTML list tags
            const activitiesList = item.activities.map(act => `
                <li style="margin-bottom: 6px; color: #495057;">${act}</li>
            `).join("");

            // Assign structural template values
            dayCard.innerHTML = `
                <h4 style="margin-top: 0; color: #212529; font-size: 1.1rem;">Day ${item.day}: ${item.theme}</h4>
                <ul style="padding-left: 20px; margin-bottom: 0;">${activitiesList}</ul>
            `;

            timeline.appendChild(dayCard);
        });

    } catch (error) {
        console.error(error);
        result.innerHTML = `<span style="color: red;">Error generating plan: ${error.message}</span>`;
    }
}); // All closing tags and loops are now properly completed here!