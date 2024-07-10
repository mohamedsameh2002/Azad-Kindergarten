
// header


document.addEventListener('scroll', function () {
    const header = document.querySelector('header');
    if (window.scrollY > 0) {
        header.classList.add('shadow-lg');
    } else {
        header.classList.remove('shadow-lg');
    }
});

document.getElementById("three-dashes").addEventListener("click", function () {
    const firstDiv = this.querySelector("div:nth-child(1)");
    const secondDiv = this.querySelector("div:nth-child(2)");
    const thirdDiv = this.querySelector("div:nth-child(3)");

    firstDiv.classList.toggle("rotate-45");
    thirdDiv.classList.toggle("-rotate-45");
    secondDiv.classList.toggle("opacity-0");

    firstDiv.classList.toggle("translate-y-3");
    thirdDiv.classList.toggle("-translate-y-3");

    document.getElementById('mobile-menu').classList.toggle('hidden')
});

// header




// memory-game 

const cards = document.querySelectorAll(".card"),
    flipsTag = document.querySelector(".flips b"),
    refreshBtn = document.querySelector(".details button"),
    memoryGameFld = document.querySelector("#memory-game-fld");
const challengeLetters = document.getElementById('challenge-letters')
let flips = 0;
let matchedCard = 0;
let disableDeck = false;
let isPlaying = false;
let cardOne, cardTwo;

function flipCard({ target: clickedCard }) {
    if (!isPlaying) {
        isPlaying = true;
    }
    if (clickedCard !== cardOne && !disableDeck) {
        flips++;
        flipsTag.innerText = flips;
        clickedCard.classList.add("flip");
        if (!cardOne) {
            return cardOne = clickedCard;
        }
        cardTwo = clickedCard;
        disableDeck = true;
        let cardOneImg = cardOne.querySelector(".back-view img").src.split('/').pop().replace(/^.*?-/, '-').match(/\d+/)[0],
            cardTwoImg = cardTwo.querySelector(".back-view img").src.split('/').pop().replace(/^.*?-/, '-').match(/\d+/)[0];

        matchCards(cardOneImg, cardTwoImg);
    }
}


function matchCards(img1, img2) {
    if (Number(img1) >= 7) {
        img1 = Number(img1) - 6
    }
    if (Number(img2) >= 7) {
        img2 = Number(img2) - 6
    }
    if (Number(img2) === Number(img1)) {
        matchedCard++;

        cardOne.removeEventListener("click", flipCard);
        cardTwo.removeEventListener("click", flipCard);
        cardOne = cardTwo = "";
        disableDeck = false;

        if (matchedCard === cards.length / 2) {
            setTimeout(() => {


                const end = Date.now() + 15 * 1000;

                // go Buckeyes!
                const colors = ["#facc15", "#ef4444"];

                (function frame() {
                    confetti({
                        particleCount: 2,
                        angle: 60,
                        spread: 55,
                        origin: { x: 0 },
                        colors: colors,
                    });

                    confetti({
                        particleCount: 2,
                        angle: 120,
                        spread: 55,
                        origin: { x: 1 },
                        colors: colors,
                    });

                    if (Date.now() < end) {
                        requestAnimationFrame(frame);
                    }
                })();

                memoryGameFld.value = flips;
            }, 500);
        }
        return;
    }

    setTimeout(() => {
        cardOne.classList.add("shake");
        cardTwo.classList.add("shake");
    }, 400);

    setTimeout(() => {
        cardOne.classList.remove("shake", "flip");
        cardTwo.classList.remove("shake", "flip");
        cardOne = cardTwo = "";
        disableDeck = false;
    }, 1200);
}

function shuffleCard() {
    flips = matchedCard = 0;
    cardOne = cardTwo = "";
    flipsTag.innerText = flips;
    disableDeck = isPlaying = false;

    let arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];
    arr.sort(() => Math.random() > 0.5 ? 1 : -1);
    const lettersGame = ['أ-ب-ت-ث-ج-ح', 'خ-د-ذ-ر-ز-س', 'ش-ص-ض-ط-ظ-ع', 'غ-ف-ق-ك-ل-م']
    const randomNumMeory = Math.floor(Math.random() * 4) + 1;
    switch (randomNumMeory) {
        case 1:
            challengeLetters.innerText = lettersGame[0]
            break;
        case 2:
            challengeLetters.innerText = lettersGame[1]
            break;
        case 3:
            challengeLetters.innerText = lettersGame[2]
            break;
        case 4:
            challengeLetters.innerText = lettersGame[3]
            break;
    }

    cards.forEach((card, index) => {
        card.classList.remove("flip");
        let imgTag = card.querySelector(".back-view img");
        setTimeout(() => {
            if (arr[index] <= 6) {
                imgTag.src = `../static/images/memory/${randomNumMeory}/img-${arr[index]}.png`;
            }
            else {
                imgTag.src = `../static/images/memory/${randomNumMeory}/Pimg-${arr[index]}.png`;
            }
        }, 500);
        card.addEventListener("click", flipCard);
    });
}

shuffleCard();

refreshBtn.addEventListener("click", shuffleCard);

cards.forEach(card => {
    card.addEventListener("click", flipCard);
});

// memory-game 




// puzzle-game 

var rows = 3;
var columns = 3;

var currTile;
var otherTile;
const randomNumPuzzle = Math.floor(Math.random() * 7) + 1;
var turns = 0;

window.onload = function () {
    // Initialize the 3x3 board
    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < columns; c++) {
            // <img>
            let tile = document.createElement("img");
            tile.src = "../static/images/puzzle/blank.png";

            // DRAG FUNCTIONALITY
            tile.addEventListener("dragstart", dragStart); // Click on image to drag
            tile.addEventListener("dragover", dragOver);   // Drag an image
            tile.addEventListener("dragenter", dragEnter); // Dragging an image into another one
            tile.addEventListener("dragleave", dragLeave); // Dragging an image away from another one
            tile.addEventListener("drop", dragDrop);       // Drop an image onto another one
            tile.addEventListener("dragend", dragEnd);     // After you completed dragDrop

            // CLICK FUNCTIONALITY
            tile.addEventListener("click", handleClick);

            document.getElementById("board").append(tile);
        }
    }

    // Pieces
    let pieces = [];
    for (let i = 1; i <= rows * columns; i++) {
        pieces.push(i.toString()); // Put "1" to "9" into the array (puzzle images names)
    }
    pieces.reverse();
    for (let i = 0; i < pieces.length; i++) {
        let j = Math.floor(Math.random() * pieces.length);

        // Swap
        let tmp = pieces[i];
        pieces[i] = pieces[j];
        pieces[j] = tmp;
    }

    for (let i = 0; i < pieces.length; i++) {
        let tile = document.createElement("img");
        tile.src = `../static/images/puzzle/${randomNumPuzzle}/${pieces[i]}.png`;

        // DRAG FUNCTIONALITY
        tile.addEventListener("dragstart", dragStart); // Click on image to drag
        tile.addEventListener("dragover", dragOver);   // Drag an image
        tile.addEventListener("dragenter", dragEnter); // Dragging an image into another one
        tile.addEventListener("dragleave", dragLeave); // Dragging an image away from another one
        tile.addEventListener("drop", dragDrop);       // Drop an image onto another one
        tile.addEventListener("dragend", dragEnd);     // After you completed dragDrop

        // CLICK FUNCTIONALITY
        tile.addEventListener("click", handleClick);

        document.getElementById("pieces").append(tile);
    }
}

// DRAG TILES
function dragStart(e) {
    currTile = this; // This refers to image that was clicked on for dragging

    // Change cursor to the image being dragged
    e.dataTransfer.setDragImage(this, 50, 50);
    document.body.style.cursor = `url(${this.src}), auto`;
}

function dragOver(e) {
    e.preventDefault();
}

function dragEnter(e) {
    e.preventDefault();
}

function dragLeave() {

}

function dragDrop() {
    otherTile = this; // This refers to image that is being dropped on
}

const boardDiv = document.getElementById('board');

function dragEnd() {
    if (currTile.src.includes("blank")) {
        return;
    }
    let currImg = currTile.src;
    let otherImg = otherTile.src;
    currTile.src = otherImg;
    otherTile.src = currImg;

    // Reset cursor to default
    document.body.style.cursor = "default";

    turns += 1;
    document.getElementById("turns").innerText = turns;

    checkPuzzleSolved();
}

// Handle click event
function handleClick() {
    if (!currTile) {
        currTile = this; // First click selects the image to be moved

    } else {
        otherTile = this; // Second click selects the target position
        // Swap images
        let currImg = currTile.src;
        let otherImg = otherTile.src;
        currTile.src = otherImg;
        otherTile.src = currImg;
        // Reset currTile
        currTile = null;

        // Increment turn counter
        turns += 1;
        document.getElementById("turns").innerText = turns;

        // Check if the puzzle is solved
        checkPuzzleSolved();
    }
}



// Check if the puzzle is solved
function checkPuzzleSolved() {
    if (`${boardDiv.outerHTML}` === `<div class="w-1/2 h-fit max-lg:w-3/4 flex flex-wrap xl:w-5/12" id="board"><img src="http://127.0.0.1:8000/static/images/puzzle/${randomNumPuzzle}/7.png"><img src="http://127.0.0.1:8000/static/images/puzzle/${randomNumPuzzle}/8.png"><img src="http://127.0.0.1:8000/static/images/puzzle/${randomNumPuzzle}/9.png"><img src="http://127.0.0.1:8000/static/images/puzzle/${randomNumPuzzle}/4.png"><img src="http://127.0.0.1:8000/static/images/puzzle/${randomNumPuzzle}/5.png"><img src="http://127.0.0.1:8000/static/images/puzzle/${randomNumPuzzle}/6.png"><img src="http://127.0.0.1:8000/static/images/puzzle/${randomNumPuzzle}/1.png"><img src="http://127.0.0.1:8000/static/images/puzzle/${randomNumPuzzle}/2.png"><img src="http://127.0.0.1:8000/static/images/puzzle/${randomNumPuzzle}/3.png"></div>`) {
        const duration = 15 * 1000,
            animationEnd = Date.now() + duration,
            defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 0 };

        function randomInRange(min, max) {
            return Math.random() * (max - min) + min;
        }

        const interval = setInterval(function () {
            const timeLeft = animationEnd - Date.now();

            if (timeLeft <= 0) {
                return clearInterval(interval);
            }

            const particleCount = 50 * (timeLeft / duration);

            // since particles fall down, start a bit higher than random
            confetti(
                Object.assign({}, defaults, {
                    particleCount,
                    origin: { x: randomInRange(0.1, 0.3), y: Math.random() - 0.2 },
                })
            );
            confetti(
                Object.assign({}, defaults, {
                    particleCount,
                    origin: { x: randomInRange(0.7, 0.9), y: Math.random() - 0.2 },
                })
            );
        }, 250);
    }
}

// puzzle-game 







import { Questions } from './questions.js';
var allQuestions = 10;
var correct = 0;
var wrong = 0;

var imageQuestion = document.getElementById('image-question');
var theQuestion = document.getElementById('the-question');
const answers = document.querySelectorAll('.answer p');

function establishAnswers() {
    const randQuesGame = Math.floor(Math.random() * Questions.length);
    imageQuestion.src = Questions[randQuesGame][4][0];
    imageQuestion.name = Questions[randQuesGame][4][1];
    theQuestion.textContent = Questions[randQuesGame][0];
    answers.forEach((answer, index) => {
        answer.textContent = Questions[randQuesGame][index + 1];
        answer.removeEventListener('click', checkAnswer);
        answer.addEventListener('click', checkAnswer);
    });
}

function checkAnswer(e) {
    const ans = e.target.textContent;
    const correctAnswer = imageQuestion.name;
    establishAnswers();
    if (correctAnswer === ans) {
        const end = Date.now() + 15 * 1000;

        confetti({
            particleCount: 100,
            spread: 70,
            origin: { y: 0.6 },
        });
        correct += 1;
        document.getElementById("the-correct").textContent = correct;
    } else {
        alert('No!!');
        wrong += 1;
        document.getElementById("the-wrong").textContent = wrong;
    }
    allQuestions -= 1;
    document.getElementById("all-questions").textContent = allQuestions;

    if (allQuestions <= 0) {
        alert('Game over!');
        // يمكن إعادة تعيين اللعبة هنا إذا كنت تريد ذلك
    }
}

establishAnswers();




// Questions-game 