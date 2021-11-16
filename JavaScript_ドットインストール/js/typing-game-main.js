'use strict'

{
    const words = [
        'apple',
        'sky',
        'blue',
        'set',
    ];
    let word;
    let loc;
    let score;
    let miss;
    // 3秒
    const timeLimit = 3 * 1000;
    let startTime;
    let isPlaying = false;

    const target = document.getElementById('target');
    const scoreLabel = document.getElementById('score');
    const missLabel = document.getElementById('miss');
    const timerLabel = document.getElementById('timer');

    function updateTarget() {
        let placeholer = '';
        for (let i = 0; i < loc; i++) {
            placeholer += '_';
        }
        target.textContent = placeholer + word.substring(loc);
    }

    function updateTImer() {
        const timeLeft = timeLimit + startTime - Date.now();
        timerLabel.textContent = (timeLeft / 1000).toFixed(2);

        const timeoutId = setTimeout(() => {
            updateTImer();
        }, 10);

        if (timeLeft < 0) {
            isPlaying = false;
            clearTimeout(timeoutId)
            timerLabel.textContent = '0.00';
            setTimeout(() => {
                showResult();
                // alert('Game Over')
            }, 100);

            target.textContent = `click to replay`;
        }
    }

    function showResult() {
        const accuracy = score + miss === 0 ? 0 : score / (score + miss) * 100;
        alert(`${score} letters, ${miss} miss, ${accuracy.toFixed(2)}% accuracy`)
    }

    window.addEventListener('click', () => {
        if (isPlaying === true){
            return;
        }
        isPlaying = true;

        loc = 0;
        score = 0;
        scoreLabel.textContent = score;
        missLabel.textContent = miss;
        word = words[Math.floor(Math.random() * words.length)];

        target.textContent = word;
        startTime = Date.now();
        updateTImer();
    })

    window.addEventListener('keydown', (e) => {
        if (isPlaying !== true) {
            return;
        }
        if (e.key === word[loc]){
            loc++
            if (loc === word.length) {
                word = words[Math.floor(Math.random() * words.length)];
                loc = 0;
            }
            updateTarget();
            score++;
            scoreLabel.textContent = score;
        } else {
            miss++;
            missLabel.textContent = miss;
        }
    })
}