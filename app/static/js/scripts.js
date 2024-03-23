const inputText = document.querySelector('#guess-country');
const flagImage = document.querySelector('#flag-discover');
const flagModal = document.querySelector('#flag-modal');
const button = document.querySelector('#button-submit')
const date = document.querySelector('#date_challenge').value;
const guesses = document.querySelectorAll('.country-guess');
const max_tries = 5;
let current = [];
let lastId = 0;
let currentFlag;
const span = document.getElementsByClassName("close")[0];


if (localStorage.getItem(date) !== null) {

    current = JSON.parse(localStorage.getItem(date));
    initial_flag();
    current.forEach((element, index) => {
        add_item(element, index);
    })
}

async function initial_flag() {
    let countries = []
    current.forEach((element) => {
        countries.push(element.country)
    })

    const request = await fetch('/initial_flag/'+countries.join(','))
    const data = await request
    const status = data.status
    const response = await request.json()

    if(status === 200) {
        flagImage.src = `data:image/png;base64, ${response.flag}`
    }
}

async function guess(){

    let countries = []
    current.forEach((element) => {
        countries.push(element.country.toLowerCase())
    })

    if(countries.includes(inputText.value.toLowerCase()))
    {
        inputText.value = ''
        return
    }

    const form = new FormData();
    form.set('country', inputText.value);
    form.set('current_flag', flagImage.src)
    const request = await fetch('/guess',{
        method: 'POST',
        body: form
    })

    const data = await request;
    const status = data.status;
    const response = await request.json()

    if(status === 200) {
        flagImage.src = `data:image/png;base64, ${response.result.guess64}`
        currentFlag = response.result.flag_base_64;
        setTimeout(changeImage, 1000);
        inputText.value = ''
        current.push({country: response.result.country, correct_percent: response.result.correct_percent})
        localStorage.setItem(date, JSON.stringify(current))
        add_item(response.result)
    }
    console.log(response);
}


function add_item(info){
    if(lastId > max_tries){
        gameOver()
        return
    }

    const countryName = document.createElement('p')
        countryName.innerText = info.country
        countryName.classList.add('guess-name')

        const progressDiv = document.createElement('div')
        progressDiv.classList.add('guess-progress')

        const progressBackground = document.createElement('div')
        progressBackground.classList.add('backgroud-progress')

        const progressBar = document.createElement('div')
        progressBar.classList.add('progress-bar')
        if(info.correct_percent > 0 && info.correct_percent < 1.5)
            progressBar.style.width = '1.5%'
        else
            progressBar.style.width = `${info.correct_percent}%`

        const percentText = document.createElement('p')
        percentText.innerText = info.correct_percent + '%'

        progressBackground.appendChild(progressBar)

        progressDiv.appendChild(progressBackground)
        progressDiv.appendChild(percentText)

        guesses[lastId].appendChild(countryName);
        guesses[lastId].appendChild(progressDiv);
        lastId++;

        if(info.correct_percent === 100)
            completeGame()
        else if(lastId > max_tries)
            gameOver()

}


function gameOver(){
    inputText.disabled = true;
    inputText.value = 'Failed!! 😞';
    button.disabled = true;
    prepareModal('Unfortunately, it didn\'t work out for today!!');
}

function completeGame(){
    inputText.disabled = true;
    inputText.value = 'Congratulations!! 🥳';
    button.disabled = true;
    prepareModal('Congratulations, you guessed today\'s flag correctly!!');
}

function changeImage() {
    flagImage.style.opacity = 0.2;

    setTimeout(() => {
        flagImage.src = `data:image/png;base64, ${currentFlag}`
    }, 500);

    setTimeout(() => {
        flagImage.style.opacity = 1;
    }, 600);
}

span.addEventListener('click', ()=> {
    document.querySelector('#myModal').style.display = 'none';
})

async function prepareModal(message) {
    const request = await fetch('/correct-answer')
    const data = await request
    const status = data.status
    const response = await request.json()

    if(status === 200) {
        flagModal.src = `data:image/png;base64, ${response.flag}`
        document.querySelector('#country-name').innerText = response.answer
        document.querySelector('#time-remaining-text').innerText = `Please come back again in ${response.time_remaining.hours} hours and ${response.time_remaining.minutes} minutes.`;
        document.querySelector('#message-result').innerText = message
        document.querySelector('#myModal').style.display = 'block';
        setTimeout(()=> {
            flagImage.src = `data:image/png;base64, ${response.flag}`
        }, 2001)
    }
}