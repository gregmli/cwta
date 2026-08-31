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

(function () {
	var lightbox = document.getElementById('image-lightbox');
	if (!lightbox) return;

	var allThumbnails = Array.prototype.slice.call(document.querySelectorAll('[data-lightbox-src]'));
	var thumbnails = [];
	var image = lightbox.querySelector('.image');
	var closeButton = lightbox.querySelector('.close');
	var currentIndex = 0;
	var previouslyFocused = null;

	function showPhoto(index) {
		currentIndex = (index + thumbnails.length) % thumbnails.length;
		image.src = thumbnails[currentIndex].getAttribute('data-lightbox-src');
		image.alt = thumbnails[currentIndex].getAttribute('data-lightbox-alt');
	}

	function openLightbox(thumbnail) {
		var gallery = thumbnail.parentNode;
		thumbnails = Array.prototype.slice.call(gallery.querySelectorAll('[data-lightbox-src]'));
		var index = thumbnails.indexOf(thumbnail);
		previouslyFocused = document.activeElement;
		showPhoto(index);
		lightbox.setAttribute('aria-hidden', 'false');
		document.body.classList.add('lightbox-open');
		closeButton.focus();
	}

	function closeLightbox() {
		lightbox.setAttribute('aria-hidden', 'true');
		document.body.classList.remove('lightbox-open');
		image.src = '';
		if (previouslyFocused) previouslyFocused.focus();
	}

	allThumbnails.forEach(function (thumbnail) {
		thumbnail.addEventListener('click', function () { openLightbox(thumbnail); });
	});

	Array.prototype.forEach.call(lightbox.querySelectorAll('[data-lightbox-close]'), function (control) {
		control.addEventListener('click', closeLightbox);
	});
	lightbox.querySelector('[data-lightbox-previous]').addEventListener('click', function () { showPhoto(currentIndex - 1); });
	lightbox.querySelector('[data-lightbox-next]').addEventListener('click', function () { showPhoto(currentIndex + 1); });

	document.addEventListener('keydown', function (event) {
		if (lightbox.getAttribute('aria-hidden') === 'true') return;
		if (event.key === 'Escape' || event.keyCode === 27) closeLightbox();
		if (event.key === 'ArrowLeft' || event.keyCode === 37) showPhoto(currentIndex - 1);
		if (event.key === 'ArrowRight' || event.keyCode === 39) showPhoto(currentIndex + 1);
	});
}());
