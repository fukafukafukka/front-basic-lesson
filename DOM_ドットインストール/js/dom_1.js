'use strict';

{
    function update() {
        // 以下全て同じように動く。
        // document.querySelector('h1').textContent = 'Changed!';
        // document.querySelector('#target').textContent = 'Changed!';
        document.getElementById('target').textContent = 'Changed!';
        // 以下、最初のp要素しか取得できないので1つしか変わらない。
        // document.querySelector('p').textContent = 'Changed!';
        // 以下は全て取得するので全て変えられる。→2番目削除している。
        // document.querySelectorAll('p')[1].textContent = 'Changed!';
        // 以下p要素全て取得し、forEachで何晩目かも出力している。
        document.querySelectorAll('p').forEach((p, index) => {
            p.textContent = `${index}番目のpです！`;
        })
    }

    setTimeout(update, 1000);
}