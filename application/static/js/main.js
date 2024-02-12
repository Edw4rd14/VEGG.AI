/*
==================================================
ST1516 DEVOPS AND AUTOMATION FOR AI CA2 ASSIGNMENT 
NAME: EDWARD TAN YUAN CHONG
CLASS: DAAA/FT/2B/04
ADM NO: 2214407
==================================================
FILENAME: main.js
==================================================
*/

// SCROLL ANIMATION
const checkVisibility = () => {
    var pageTop = $(document).scrollTop();
    var pageBottom = pageTop + $(window).height();
    var tags = $(".fade");
    tags.each(function() {
        var tag = $(this);
        var marginTop = parseInt(tag.css('margin-top'), 10);
        var effectiveTop = tag.offset().top - marginTop;
        if (effectiveTop < pageBottom && (effectiveTop + tag.outerHeight() > pageTop)) {
            tag.addClass("visible");
        } else {
            tag.removeClass("visible");
        }
    });
}

// CALL CHECKVISIBILITY FUNCTION ON SCROLL
$(document).on("scroll", checkVisibility);

// ALSO CALL CHECKVISIBILITY FUNCTION AS SOON AS THE PAGE LOADS
$(document).ready(checkVisibility);