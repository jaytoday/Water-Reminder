
$(document).ready(function(){

  /*

     $('#slidesContainer a').lightBox({
	overlayBgColor: '#666',
	overlayOpacity: 0.6,
	containerResizeSpeed: 350
   });
   
  */  
     $('#slidesContainer a').click(function(){

       if ($('#controls').find('.active:last').attr('id') === 'leftControl')
       actionControl = $('#leftControl');
       
       if ($('#controls').find('.active:first').attr('id') === 'rightControl')
       actionControl = $('#rightControl');

       actionControl.click();
     });
     
     
  // set vars 
  var currentPosition = 0;
  var slideWidth = 950;
  var slides = $('.slide');
  var numberOfSlides = slides.length;
  var imgShowClass = 'imgShowClass';
  
  // Remove scrollbar in JS
  $('#slidesContainer').css('overflow', 'hidden');

  // Wrap all .slides with #slideInner div
  slides.wrapAll('<div id="slideInner"><div>')
    
    // Float left to display horizontally, readjust .slides width
        .css({
      'float' : 'left',
      'width' : slideWidth
    });

  // Set #slideInner width equal to total width of all slides
  $('#slideInner').css('width', slideWidth * numberOfSlides);

  // Create event listeners for .controls clicks
  $('.control')
    .bind('click', function(){
    if (! $(this).hasClass('active')) return;
    // Determine new position
    currentPosition = ($(this).attr('id')=='rightControl') ? currentPosition+1 : currentPosition-1;
    
    // Hide / show controls
    manageControls(currentPosition);
    
    // Move slideInner using margin-left
    hideImage();
    $('#slideInner').animate({
      'marginLeft' : slideWidth*(-currentPosition)
    }, 1000);
    showImage(currentPosition);
    
  });


  function hideImage(){
      $('#slideInner')
     .find('.' + imgShowClass).removeClass(imgShowClass).fadeOut(500);
  }
  
  function showImage(position){
     var this_slide = $('#slideInner').find('.slide:eq(' + position + ')');
     addImgAttr(this_slide);
     this_slide.find('.imageContainer:first').addClass(imgShowClass).fadeIn(1200);
     var next_slide = this_slide.next();
     if (next_slide) setTimeout(function(){ 
       addImgAttr(next_slide);
       }, 500);
  };
  
  function addImgAttr(slide){
         slide.find('img').each(function(){
        if (!$(this).attr('src'))
        $(this).attr('src', $(this).attr('_src')); 
      });
  }
  
  showImage(currentPosition);

  // manageControls: Hides and Shows controls depending on currentPosition
  function manageControls(position){
    // Hide left arrow if position is first slide
        if(position==0){ $('#leftControl').removeClass('active').find('img').hide() } 
        else{ $('#leftControl').addClass('active').find('img').show() }
        // Hide right arrow if position is last slide
    if(position==numberOfSlides-1){ $('#rightControl').removeClass('active').find('img').hide() } 
    else{ $('#rightControl').addClass('active').find('img').show() }
  }     
  
});
