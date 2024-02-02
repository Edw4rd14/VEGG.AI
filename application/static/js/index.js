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

// IMAGE UPLOAD
const dropArea = document.getElementById('drop-area')
const imageFile = document.getElementById('image-file')
const imgView = document.getElementById('img-view')

imageFile.addEventListener('change', uploadImage);

uploadImage = () => {
    let imgLink = URL.createObjectURL(imageFile.files[0]);
    imgView.style.backgroundImage = `url(${imgLink})`;
}