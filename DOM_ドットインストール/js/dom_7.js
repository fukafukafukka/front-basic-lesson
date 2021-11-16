'use strict';

{
  document.querySelector('button').addEventListener('click', () => {
    const item1 = document.querySelectorAll('li')[1];

    // 一部の古いブラウザでは使えない。
    // item1.remove();

    // 親Node.removeChilde(削除するNode)
    document.querySelector('ul').removeChild(item1);
  });
}