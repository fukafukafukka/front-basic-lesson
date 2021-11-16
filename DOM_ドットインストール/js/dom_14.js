'use strict';

{
  document.querySelector('form').addEventListener('submit', (e) => {
    // 以下のメソッドでページ遷移をキャンセルしている。これによってコンソール上にsubmitの文字が表示されたままになる。
    e.preventDefault();
    console.log('submit');
  })
}