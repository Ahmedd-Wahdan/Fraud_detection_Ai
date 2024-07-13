function onSubmit() {
    // Prevent form submission
   var amount = document.forms["myForm"]["amount"];
   var transactionDate = document.forms["myForm"]["transactiondate"];
   var transactionTime = document.forms["myForm"]["transactiontime"];
   var category = document.forms["myForm"]["category"];
   var currentDate = new Date();

   var dataValidated = true;

   // Validate form fields
   if (amount.value === '' || transactionDate.value === '' || transactionTime.value === '' || category.value === '') {
       alert("Please fill all the required data!");
       dataValidated = false;
   }

   if (isNaN(amount.value)) {
       alert("Please enter a valid amount!");
       dataValidated = false;
   }

   var inputDate = new Date(transactionDate.value + 'T' + transactionTime.value);
   if (inputDate > currentDate) {
       alert("enter valid date");
       dataValidated = false;
   }

   if (dataValidated) 
   {
       // Collect user input data from form
       var form = document.getElementById("myForm");
       var formData = {};

       // Loop through each form element
       for (var i = 0; i < form.elements.length; i++) 
       {
         var element = form.elements[i];
         // Check if the element is an input field with a name
         if (element.tagName === 'INPUT'||element.tagName === 'SELECT') 
           {
           formData[element.name] = element.value;
           }
       }
       console.log(formData);

       // Send a POST request to the server (Flask) for prediction
       fetch("/hello", {
           method: "POST",
           headers: {
               'Content-Type': 'application/json'
           },
           body: JSON.stringify(formData)
       })
       .then(response => response.json())
       .then(data => 
       {
           console.log("Data:", data.prediction);
           //message with the alert
           alert("Prediction: " + data.prediction);
           
           // Display the prediction result on the page
           // document.getElementById("result-text").textContent = data.result;
           // Reset the form to clear previous input
           // document.getElementById("prediction-form").reset();
       })
       .catch(error => console.error("Error:", error));
    }
}