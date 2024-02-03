/*
==================================================
ST1516 DEVOPS AND AUTOMATION FOR AI CA2 ASSIGNMENT 
NAME: EDWARD TAN YUAN CHONG
CLASS: DAAA/FT/2B/04
ADM NO: 2214407
==================================================
FILENAME: layout.html
==================================================
*/


// SCROLL ANIMATION
function checkVisibility() {
    var pageTop = $(document).scrollTop();
    var pageBottom = pageTop + $(window).height();
    var tags = $(".fade");
  
    for (var i = 0; i < tags.length; i++) {
        var tag = tags[i];
  
        // Element's bottom position
        var tagBottom = $(tag).position().top + $(tag).outerHeight();
  
        // Add 'visible' class if any part of the element is in the viewport
        if (tagBottom > pageTop && $(tag).position().top < pageBottom) {
            $(tag).addClass("visible");
        } else {
            // Remove 'visible' class only if the element is completely out of the viewport
            $(tag).removeClass("visible");
        }
    }
  }

// CALL CHECKVISIBILITY FUNCTION ON SCROLL
$(document).on("scroll", checkVisibility);
// ALSO CALL CHECKVISIBILITY FUNCTION AS SOON AS THE PAGE LOADS
$(document).ready(checkVisibility);

// TO CLASSIFIER BUTTON ON CLICK
document.getElementById('tc-button').addEventListener('click', () => {
    const element = document.getElementById('classifier-title');
    const headerOffset = 100;
    const elementPosition = element.getBoundingClientRect().top + window.scrollY;
    const offsetPosition = elementPosition - headerOffset;
    window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
    });
});

// IMAGE UPLOAD
const dropArea = document.getElementById('drop-area')
const imageFile = document.getElementById('image-file')
const imgView = document.getElementById('img-view')

uploadImage = () => {
    let imgLink = URL.createObjectURL(imageFile.files[0]);
    imgView.style.backgroundImage = `url(${imgLink})`;
    imgView.textContent = "";
    imgView.style.backgroundColor = 'white';
}

// DRAG AND DROP
dropArea.addEventListener('dragover', (e)=>{
    e.preventDefault();
})

dropArea.addEventListener('drop', (e) => {
    e.preventDefault();
    // Check if any files were dropped
    if (e.dataTransfer.items) {
        // Use DataTransferItemList interface to access the file(s)
        for (let i = 0; i < e.dataTransfer.items.length; i++) {
            // If dropped items are not files, ignore
            if (e.dataTransfer.items[i].kind === 'file') {
                var file = e.dataTransfer.items[i].getAsFile();
                // Only handle first file
                let imgLink = URL.createObjectURL(file);
                imgView.style.backgroundImage = `url(${imgLink})`;
                imgView.textContent = "";
                imgView.style.backgroundColor = 'white';
                // Exit the loop after handling the first file
                break; 
            }
        }
    } else {
        // Use DataTransfer interface to access the file(s)
        let imgLink = URL.createObjectURL(e.dataTransfer.files[0]);
        imgView.style.backgroundImage = `url(${imgLink})`;
        imgView.textContent = "";
        imgView.style.backgroundColor = 'white';
    }
});

imageFile.addEventListener('change', uploadImage);


// FUNCTION TO MAKE SUBMIT BUTTON SCROLL TO FORM UPON REFRESH
function rememberRedirectTarget(target) {
    // Store the ID of the form which I want the website to redirect to upon refresh
    sessionStorage.setItem('redirectTarget', target);
}
// Check stored target existence, if it exists redirect
window.onload = function() {
    // Get redirect ID
    const redirectTarget = sessionStorage.getItem('redirectTarget');
    // If it exists
    if (redirectTarget) {
        // Scroll to the target element
        const targetElement = document.getElementById(redirectTarget);
        if (targetElement) {
            targetElement.scrollIntoView();
            window.scrollBy(0, -100);
            // Reset stored redirect ID so it can be reused
            sessionStorage.removeItem('redirectTarget');
        }
    }
};