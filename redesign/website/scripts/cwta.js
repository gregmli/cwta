function updateNavbar() {
	var viewTop = $(window).scrollTop()
    var viewBottom =  viewTop + $(window).height();

    var elemBottom = $('.photobar.title').offset().top + $('.photobar.title').height();
    var elemTop = elemBottom - $('#navbar').height();
	
    $('.photobar.title').toggleClass('navbar-bottom', viewBottom < elemBottom);
    $('.photobar.title').toggleClass('navbar-scroll', viewTop <= elemTop && elemBottom <= viewBottom);
    $('.photobar.title').toggleClass('navbar-top', elemTop < viewTop);
    
}


function updateMap() {
	var map = $('.photobar.contact .location .map'); 
	var mapImg = $('.photobar.contact .location .map img');
	
	var leftPos = -(mapImg.width()/2 - map.width()/2);
	var topPos = -(mapImg.height()/2 - map.height()/2);
	
	// doesn't work if image isn't loaded.. arg..
	alert(leftPos +", "+ topPos);
	
	mapImg.css({left: leftPos, top:topPos});
}
