$(function() {
  var interval = 6000;
  $('.slideshow').each(function() {
    var timer;
    var container = $(this);

    function switchImg() {
      var anchors = container.find('a');
      var first = anchors.eq(0);
      var second = anchors.eq(1);
      first.appendTo(container).fadeOut(3000);
      second.fadeIn(3000);
    }

    function startTimer() {
      timer = setInterval(switchImg, interval);
    }

    function stopTimer() {
      clearInterval(timer);
    }
    container.find('a').hover(stopTimer, startTimer);
    startTimer();
  });
});
