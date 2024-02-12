/*
==================================================
ST1516 DEVOPS AND AUTOMATION FOR AI CA2 ASSIGNMENT 
NAME: EDWARD TAN YUAN CHONG
CLASS: DAAA/FT/2B/04
ADM NO: 2214407
==================================================
FILENAME: signup.js
==================================================
*/

// LOGIN POP-UP
// Function to toggle the popup
const togglePopup = () => {
    document.getElementById("signupPopup").classList.toggle("active");
}
  
const closePopupOnClickOutside = (e) => {
    var signupPopup = document.getElementById("signupPopup");
    // Check if the click is outside the popup container
    if (e.target === signupPopup) {
        togglePopup();
    }
}

// Ensuring the button exists before adding event listener
var signupButton = document.getElementById("signupButton");
// Adding click event listener to the overlay to close the popup when clicked outside
var signupPopup = document.getElementById("signupPopup");
// Preventing popup from closing when clicking inside the popup container
var popupContainer = document.querySelector(".popup-container");

// Close pop-up on click
signupPopup.addEventListener("click", closePopupOnClickOutside);
// Toggle pop-up on click
signupButton.addEventListener("click", togglePopup);
// Prevent closing when clicking within popup container
popupContainer.addEventListener("click", (e) => {
    e.stopPropagation();
});

// Edit footer to be at the bottom
var footer = document.getElementById('footer');
footer.style.position = 'absolute';
footer.style.bottom = '0';