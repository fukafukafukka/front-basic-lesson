'use strict';

{
  document.querySelector('button').addEventListener('click', () => {
    const colors = document.querySelectorAll('input');
    const selectedColors = [];

    colors.forEach(color => {
      if (color.checked === true){
        selectedColors.push(color.value);
      }
    });

    const li = document.createElement('li');
    // li.textContent = selectedColors.join(',');
    // 上と同じ意味。配列が文字列に変換されるときは自動でカンマ区切りで変換される。
    li.textContent = selectedColors;
    document.querySelector('ul').appendChild(li);
  });
}