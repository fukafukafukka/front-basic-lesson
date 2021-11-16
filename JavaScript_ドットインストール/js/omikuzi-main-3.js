'use strict';

{
    const btn = document.getElementById('btn');

    btn.addEventListener('click', () =>{
        // omikuzi-main-2.jsのやつ。
        // const results = ['大吉', '中吉', '凶', '末吉'];
        // btn.textContent = results[Math.floor(Math.random() * results.length)];
        // 確率を変える方法1
        // const results = ['大吉', '大吉', '凶', '大吉'];
        // btn.textContent = results[Math.floor(Math.random() * results.length)];
        // 確率を変える方法2
        const n = Math.random();
        if (n < 0.05) {
            btn.textContent = '大吉'; // 5%
        } else if (n < 0.2) {
            btn.textContent = '中吉'; // 15%
        } else {
            btn.textContent = '凶'; // 80%
        }
    })
}