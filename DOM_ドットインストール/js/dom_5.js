'use strict';

{
    document.querySelector('button').addEventListener('click', () => {
        const targetNode = document.getElementById('target');

        // targetNode.textContent = 'Dotinstall';

        // 上記と同じ意味であるが、JavaScriptのデータカスタム属性を使って値を代入している例。
        targetNode.textContent = targetNode.dataset.translation;
    });

}