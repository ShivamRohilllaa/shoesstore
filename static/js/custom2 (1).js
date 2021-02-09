 
  $('.owl-carousel').owlCarousel({
    loop: true,
    margin: 10,
    nav: true,
    navText: [
        "<i class='fa fa-caret-left'></i>",
        "<i class='fa fa-caret-right'></i>"
    ],
    autoplay: true,
    autoplayHoverPause: true,
    responsive: {
        0: {
            items: 1
        },
        600: {
            items: 3
        },
        1000: {
            items: 7
        }
        ,
        1320: {
            items: 7
        }
    }
})



$('#owl-carousel').owlCarousel({
    loop: true,
    margin: 30,
    dots: true,
    nav: true,
    items: 2,
})
