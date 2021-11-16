'use strict';

{
    document.querySelector('button').addEventListener('click', () => {
        const targetNode = document.getElementById('target');

        // JSからstyleを設定してあげる。
        // targetNode.style.color = 'red';
        // targetNode.style.backgroundColor = 'skyblue';

        // htmlに記載のcssのstyleを適用させてあげる。
        // targetNode.className = 'my-color my-border';

        // htmlに設定済みのcssのsスタイルに追加でstyleを設定してあげる。
        // targetNode.className.add('my-color');

        // containsメソッドでクラスが適用されているかどうか確認する。
        // if (targetNode.classList.contains('my-color') === true){
        //     targetNode.classList.remove('my-color');
        // } else {
        //     targetNode.classList.add('my-color');
        // }

        // 上のと同じ。
        targetNode.classList.toggle('my-color');
    });

}