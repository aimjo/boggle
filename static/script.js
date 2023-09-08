 // Initialize the score, timer, and game count variables
 let score = 0;
 let timerSeconds = 60;
 let gameCount = 0;
 let highestScore = 0;

 // Function to update the timer display
 function updateTimer() {
     $('#timer').text('Time Left: ' + timerSeconds + ' seconds');
 }

 // Function to handle the countdown timer
 function startTimer() {
     const timerInterval = setInterval(function() {
         if (timerSeconds > 0) {
             timerSeconds--;
             updateTimer();
         } else {
             // Disable the input field and submit button after 60 seconds
             $('#guess').prop('disabled', true);
             $('#submit-button').prop('disabled', true);
             clearInterval(timerInterval); // Stop the timer

             // Send a request to the server with the score
             sendScoreToServer(score);
         }
     }, 1000); // Update every second
 }

 // Function to send the score to the server when the game ends
 function sendScoreToServer(score) {
     axios.post('/update_score', { score: score })
         .then(function(response) {
             // Update the game count and highest score based on the server's response
             gameCount = response.data.game_count;
             highScore = response.data.high_score;

             // Display the game count, highest score, and total games on the page
             $('#game-count').text('Total Games Played: ' + gameCount);
             $('#high-score').text('High Score: ' + highScore);
             $('#total-games').text('Total Games Played: ' + gameCount);
         })
         .catch(function(error) {
             console.error(error);
         });
 }

// Function to reset the board
function resetBoard() {
    // Reset the timer and re-enable input field and submit button
    timerSeconds = 60;
    updateTimer();
    $('#guess').prop('disabled', false);
    $('#submit-button').prop('disabled', false);

    // Send a request to the server to generate a new board
    axios.get('/reset_board')
        .then(function(response) {
            // Update the board with the new one received from the server
            const board = response.data.board;
            $('#current-score').text('Score: 0'); // Reset the score to 0
            score = 0;
            updateBoard(board);
        })
        .catch(function(error) {
            console.error(error);
        });
}

// Function to update the board display
function updateBoard(board) {
    // Update the table cells with the new board data
    // This code should recreate the table structure and update the cell values
    // You can use a similar approach as when initially displaying the board.
    // Here, I'm assuming your board is a 2D array, similar to the initial display.
    const table = $('#board-table');
    table.empty(); // Clear the existing table

    for (const row of board) {
        const tr = $('<tr></tr>');
        for (const cell of row) {
            const td = $('<td></td>').text(cell);
            tr.append(td);
        }
        table.append(tr);
    }
}

// Handle form submission via AJAX
$(document).ready(function() {
    // Attach the click event handler to the reset button
    $('#reset-board').click(resetBoard);

    $('#guess-form').submit(function(event) {
        event.preventDefault(); // Prevent form submission (page refresh)
        const guess = $('#guess').val(); // Get the user's guess from the form

        // Send the guess to the server using Axios
        axios.post('/check_guess', { guess: guess })
            .then(function(response) {
                const result = response.data.result;
                const message = response.data.message;

                // Clear the input field after each submission
                $('#guess').val('');

                if (result === 'ok') {
                    // Update the score with the length of the valid word
                    score += guess.length;

                    // Display the updated score on the page
                    $('#current-score').text('Score: ' + score);
                }

                // Display the result message on the page
                const resultMessage = {
                    'ok': 'Valid word on the board!',
                    'not-on-board': 'Valid word, but not on the board.',
                    'not-a-word': 'Not a valid word.'
                }[result];

                $('#guess-result').text(message);
            })
            .catch(function(error) {
                console.error(error);
            });
    });

    // Start the countdown timer when the page loads
    startTimer();
});