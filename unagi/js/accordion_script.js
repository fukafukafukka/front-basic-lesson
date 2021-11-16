$(function() {

  //.accordion2の中のp要素がクリックされたら
  $('.accordion dt').click(function() {

    //クリックされた.accordionの中のp要素に隣接する.accordionの中の.innerを開いたり閉じたりする。
    $(this).next('.accordion dd').slideToggle();

    //クリックされた.accordionの中のp要素以外の.accordionの中のp要素に隣接する.accordionの中の.innerを閉じる
    $('.accordion dt').not($(this)).next('.accordion dd').slideUp();

  });
});
