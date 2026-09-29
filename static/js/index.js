window.HELP_IMPROVE_VIDEOJS = false;

$(document).ready(function() {
  // Same responsive navbar behavior as the Nerfies template.
  $(".navbar-burger").click(function() {
    $(".navbar-burger").toggleClass("is-active");
    $(".navbar-menu").toggleClass("is-active");
  });

  // Same Bulma carousel configuration used by the Nerfies template.
  var options = {
    slidesToScroll: 1,
    slidesToShow: 3,
    loop: true,
    infinite: true,
    autoplay: false,
    autoplaySpeed: 3000,
  };

  if (typeof bulmaCarousel !== 'undefined') {
    bulmaCarousel.attach('.carousel', options);
  }
});
