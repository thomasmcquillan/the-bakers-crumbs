// Function that enables the addition of extra input fields for adding 
//      extra recipe ingredients and/or cooking steps
var addIngredient = document.getElementById('add-ingredient-btn');
var delIngredient = document.getElementById('del-ingredient-btn');

// And the location in the template where div will be inserted..
var foodDelivery = document.getElementById('food-delivery');

// On-click button listener function for actioning the dynamic
//      ingredient list on the add recipe page.
addIngredient.onclick = function(){
    var addFoodstuff = document.createElement('textarea');
    addFoodstuff.setAttribute('class', 'ingredient-list validate form-control text-center');
    addFoodstuff.setAttribute('type', 'text');
    addFoodstuff.setAttribute('name', 'ingredients');
    addFoodstuff.setAttribute('minlength', '3');
    addFoodstuff.setAttribute('style', 'height:54px');
    addFoodstuff.setAttribute('required', 'true');
    addFoodstuff.setAttribute('placeholder', 'Next ingredient goes here');
    foodDelivery.appendChild(addFoodstuff);
};

delIngredient.onclick = function(){
    var ingredient_fields = document.getElementsByClassName('ingredient-list');
    if(ingredient_fields.length > 1) {
        foodDelivery.removeChild(ingredient_fields[(ingredient_fields.length) - 1]);
    }
};

/**Below is the functionality for adding additional cooking step fields to the add_recipe page */
var nextStepButton = document.getElementById('add-step-button');
var removeStepButton = document.getElementById('remove-step-button');
var recipeDirectionsDiv = document.getElementById('recipe-directions-section');

 // Function to add further textarea fields for cooking instructions when 
 // button is clicked to enter an instruction.
 // https://www.youtube.com/watch?v=MLBLsxcB3Dc
 
nextStepButton.onclick = function(){
    var addStepButton = document.createElement('textarea');
    addStepButton.setAttribute('type', 'text');
    addStepButton.setAttribute('name', 'directions');
    addStepButton.setAttribute('class', 'recipe-directions validate form-control');
    addStepButton.setAttribute('minlength', '3');
    addStepButton.setAttribute('maxlength', '222');
    addStepButton.setAttribute('required', 'true');
    addStepButton.setAttribute('title', 'Add the next step here');
    recipeDirectionsDiv.appendChild(addStepButton);
};

removeStepButton.onclick = function(){
    var stepItems = document.getElementsByClassName('recipe-directions');
    if(stepItems.length > 1) {
        recipeDirectionsDiv.removeChild(stepItems[(stepItems.length) - 1]);
    }
};
