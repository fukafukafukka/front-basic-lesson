'use strict';

{
  document.querySelector('button').addEventListener('click', () => {
    const item0 = document.querySelectorAll('li')[0];
    const copy = item0.cloneNode(true);

    const ul = document.querySelector('ul');
    const item2 = document.querySelectorAll('li')[2];

    // copyをitem2の前にインサートする。
    ul.insertBefore(copy, item2);
  });
}