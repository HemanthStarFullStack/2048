document.addEventListener('DOMContentLoaded', (event) => {
    // The board data is passed from the Django template.
    const boardData = JSON.parse(document.getElementById('board-data').textContent);
    let board = boardData.board;
    let score = boardData.score;

    const boardElement = document.getElementById('board');
    const scoreElement = document.getElementById('score');

    function updateBoard() {
        // Clear the board
        boardElement.innerHTML = '';
        scoreElement.textContent = score;

        for (let r = 0; r < 4; r++) {
            for (let c = 0; c < 4; c++) {
                let tile = document.createElement('div');
                tile.classList.add('tile');
                let num = board[r][c];
                if (num > 0) {
                    tile.textContent = num;
                    tile.classList.add('x' + num.toString());
                }
                boardElement.append(tile);
            }
        }
    }

    updateBoard();

    document.addEventListener('keyup', (e) => {
        let url;
        if (e.code == "ArrowLeft") {
            url = '/moveleft/';
        }
        else if (e.code == "ArrowRight") {
            url = '/moveright/';
        }
        else if (e.code == "ArrowUp") {
            url = '/moveup/';
        }
        else if (e.code == "ArrowDown") {
            url = '/movedown/';
        } else {
            return;
        }

        fetch(url, {
            method: 'POST', // The views expect POST
            headers: {
                'X-CSRFToken': getCookie('csrftoken'), // Django CSRF token
                'Content-Type': 'application/json'
            },
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            board = data.board;
            score = data.score;
            updateBoard();
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
            alert('An error occurred while making a move. Please try again.');
        });
    });

    // Function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
