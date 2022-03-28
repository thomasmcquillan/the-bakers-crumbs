// hover function for custom search icon
$(document).ready(function() {
	$("#icon-wrap").hover(function() {
		$("#tbc-search-hover").toggle();
	}, function() {
		$("#tbc-search-hover").toggle();
	});
});

// Function that enables the addition of extra input fields for adding 
//      extra recipe ingredients and/or cooking steps
var add_ingredient_btn = document.getElementById('add-ingredient-btn');
var del_ingredient_btn = document.getElementById('del-ingredient-btn');

// And the location in the template where div will be inserted..
var food_delivery = document.getElementById('food-delivery');

// On-click button listener function for actioning the dynamic
//      ingredient list on the add recipe page.
add_ingredient_btn.onclick = function(){
    var addFoodstuff = document.createElement('input');
    addFoodstuff.setAttribute('id', 'ingredients');
    addFoodstuff.setAttribute('class', 'ingredient-items');
    addFoodstuff.setAttribute('type', 'text');
    addFoodstuff.setAttribute('name', 'ingredients');
    addFoodstuff.setAttribute('minlength', '3');
    addFoodstuff.setAttribute('required', 'true');
    addFoodstuff.setAttribute('placeholder', 'Add any further ingredients');
    food_delivery.appendChild(addFoodstuff);
};


del_ingredient_btn.onclick = function(){
    var ingredient_fields = document.getElementsByClassName('ingredient-list');
    if(ingredient_fields.length > 1) {
        food_delivery.removeChild(ingredient_fields[(ingredient_fields.length) - 1]);
    }
};

/**Below is the functionality for adding additional cooking step fields to the add_recipe page */
var add_step_button = document.getElementById('add-step-button');
var remove_step_button = document.getElementById('remove-step-button');
var recipe_directions_section = document.getElementById('recipe-directions-section');

 // Function to add further textarea fields for cooking instructions when 
 // button is clicked to enter an instruction.
 // https://www.youtube.com/watch?v=MLBLsxcB3Dc
 
add_step_button.onclick = function(){
    var addStepButton = document.createElement('input');
    addStepButton.setAttribute('id', 'recipe_directions');
    addStepButton.setAttribute('type', 'text');
    addStepButton.setAttribute('name', 'directions');
    addStepButton.setAttribute('class', 'validate directions');
    addStepButton.setAttribute('minlength', '3');
    addStepButton.setAttribute('required', 'true');
    addStepButton.setAttribute('placeholder', 'Add Next Step..');
        recipe_directions_section.appendChild(addStepButton);
};

remove_step_button.onclick = function(){
    var step_items = document.getElementsByClassName('recipe_directions');
    if(step_items.length > 1) {
        recipe_directions_section.removeChild(step_items[(step_items.length) - 1]);
    }
};

