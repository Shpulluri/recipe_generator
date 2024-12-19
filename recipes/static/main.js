document.addEventListener("DOMContentLoaded", () => {
    const ingredientInput = document.getElementById("ingredient-input");
    const addIngredientButton = document.getElementById("add-ingredient");
    const ingredientsDisplay = document.getElementById("ingredients-display");
    const ingredientsField = document.getElementById("ingredients");

    let ingredients = []; // Array to store ingredients

    // Function to update the hidden input field
    const updateIngredientsField = () => {
        ingredientsField.value = ingredients.join(",");
         console.log("Hidden Input Updated:", ingredientsField.value);// Store ingredients as a comma-separated string
    };

    // Function to update the visible list of ingredients
    const updateIngredientsDisplay = () => {
        ingredientsDisplay.innerHTML = ""; // Clear the existing list

        // Add each ingredient to the display list
        ingredients.forEach((ingredient, index) => {
            const listItem = document.createElement("li");
            listItem.className = "list-group-item d-flex justify-content-between align-items-center";
            listItem.textContent = ingredient;

            // Add a remove button
            const removeButton = document.createElement("button");
            removeButton.className = "btn btn-sm btn-danger";
            removeButton.textContent = "×";
            removeButton.addEventListener("click", () => {
                // Remove the ingredient from the array
                ingredients.splice(index, 1);

                // Update the hidden input field and visible list
                updateIngredientsField();
                updateIngredientsDisplay();
            });

            listItem.appendChild(removeButton); // Add the remove button to the list item
            ingredientsDisplay.appendChild(listItem); // Add the list item to the display
        });
    };

    // Add ingredient to the list when the "+" button is clicked
    addIngredientButton.addEventListener("click", () => {
        const ingredient = ingredientInput.value.trim();
        if (ingredient) {
            ingredients.push(ingredient); // Add the ingredient to the array
            ingredientInput.value = ""; // Clear the input field

            // Update the hidden input field and visible list
            updateIngredientsField();
            updateIngredientsDisplay();
        }
    });

    // Allow pressing "Enter" to add ingredients
    ingredientInput.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
            event.preventDefault();
            addIngredientButton.click(); // Trigger the "+" button click
        }
    });
});
