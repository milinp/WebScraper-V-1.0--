function EasyPeasyParallax() {
    scrollPos = $(this).scrollTop();
    $('#banner').css({
        'background-position' : '50% ' + (-scrollPos/4)+"px"
    });
     $('#content-container').css({
        'background-position' : '50% ' - (-scrollPos/4)+"em"
    });
    $('#bannertext').css({
        'margin-top': (scrollPos/4)+"px",
        'opacity': 1-(scrollPos/100),
    });
    $('#bannertext-logo').css({
        'margin-left': (scrollPos/37.5)+"em",
        'opacity': 0+(scrollPos/500),
    });
    $('#bannerlogo').css({
        'opacity': 1-(scrollPos/30),
    });
}

function autoHideBannerText(){
    var scrollPos = $(this).scrollTop();
    if ( scrollPos > 258) {
        $('#bannertext').css('visibility','hidden');
    } else {
        $('#bannertext').css('visibility','visible');
    }
}

function autoHideLogo(){
    var scrollPos = $(this).scrollTop();
    if ( scrollPos > 600){
        $('#bannertext-logo').animate({opacity: 1, marginLeft: "1em"}, 400);
    }
    else {
        $('#bannertext-logo').animate({opacity: 0, marginLeft: "-1em"}, 400);
    }
}

$(document).ready(function(){
    $(window).scroll(function() {
        EasyPeasyParallax();
        autoHideBannerText();
    });

    $('#bannertext').hover(
    function(){
        $(this).toggleClass('shadow');
    });

    $('#bannertext-logo').hover(
    function(){
        $(this).toggleClass('shadow');
    });

    $("#bannertext").click(function (){
            $('html, body').animate({
                scrollTop: $("#content").offset().top
            }, 1000, 'swing');
    });

});