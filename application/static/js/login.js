/*
==================================================
ST1516 DEVOPS AND AUTOMATION FOR AI CA2 ASSIGNMENT 
NAME: EDWARD TAN YUAN CHONG
CLASS: DAAA/FT/2B/04
ADM NO: 2214407
==================================================
FILENAME: login.js
==================================================
*/

// LOGIN POP-UP
// Function to toggle the popup
const togglePopup = () => {
    document.getElementById("loginPopup").classList.toggle("active");
}
  
const closePopupOnClickOutside = (e) => {
    var loginPopup = document.getElementById("loginPopup");
    // Check if the click is outside the popup container
    if (e.target === loginPopup) {
        togglePopup();
    }
}

// Ensuring the button exists before adding event listener
var openPopupButton = document.getElementById("openPopup");
// Adding click event listener to the overlay to close the popup when clicked outside
var loginPopup = document.getElementById("loginPopup");
// Preventing popup from closing when clicking inside the popup container
var popupContainer = document.querySelector(".popup-container");

// Close pop-up on click
loginPopup.addEventListener("click", closePopupOnClickOutside);
// Toggle pop-up on click
openPopupButton.addEventListener("click", togglePopup);
// Prevent closing when clicking within popup container
popupContainer.addEventListener("click", (e) => {
    e.stopPropagation();
});

// Edit footer to be at the bottom
var footer = document.getElementById('footer');
footer.style.position = 'absolute';
footer.style.bottom = '0';