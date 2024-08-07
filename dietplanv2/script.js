document.getElementById('disliked_foods').addEventListener('change', function() {
    const dislikedFoodsListGroup = document.getElementById('disliked_foods_list_group');
    if (this.value === 'Yes') {
        dislikedFoodsListGroup.style.display = 'block';
    } else {
        dislikedFoodsListGroup.style.display = 'none';
    }
});

document.getElementById('diet-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    const userData = {};
    formData.forEach((value, key) => {
        userData[key] = value;
    });

    fetch('/generate_diet_plan', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
    })
    .then(response => response.json())
    .then(data => {
        const dietPlanContainer = document.getElementById('diet-plan');
        const dietPlan = data.diet_plan.split('\n').map(line => `<p>${line}</p>`).join('');
        dietPlanContainer.innerHTML = `<div class="diet-plan-content">${dietPlan}</div>`;
    })
    .catch(error => console.error('Error:', error));
});
