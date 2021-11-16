'use strict';

{
  const text = document.querySelector('textarea');

  // インプットボックスにカーソルを入れるとイベントが発生する。
  // text.addEventListener('focus', () => {
  //   console.log('focus');
  // });

  // インプットボックスからカーソル が出るとイベントが発生する。
  // text.addEventListener('blur', () => {
  //   console.log('blur');
  // });

  // 値が変更されるとイベント発生する。
  text.addEventListener('input', () => {
    console.log(text.value.length);
  });

  // インプットボックスからカーソル が出るとイベントが発生する。
  text.addEventListener('change', () => {
    console.log('change');
  });
}