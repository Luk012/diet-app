document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('diet-form');
    const dietPlanContainer = document.getElementById('diet-plan');
    const dislikedFoodsField = document.getElementById('disliked_foods');
    const dislikedFoodsListContainer = document.getElementById('disliked_foods_list_container');

    dislikedFoodsField.addEventListener('change', () => {
        if (dislikedFoodsField.value === 'Yes') {
            dislikedFoodsListContainer.style.display = 'block';
        } else {
            dislikedFoodsListContainer.style.display = 'none';
        }
    });

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        const response = await fetch('http://localhost:5000/api/generate-diet-plan', { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        dietPlanContainer.textContent = result.diet_plan;
    });
});
