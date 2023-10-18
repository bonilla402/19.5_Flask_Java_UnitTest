class BoggleGame {

    constructor() {
        
        this.counter = 10;
        this.score = 0;
        this.foundWords = new Set();

        this.showtimer(this.counter);


        this.form = document.getElementById("WordForm");
        this.form.addEventListener('submit', this.HandleWordInput.bind(this));
        const boundTimer = this.startGameTimer.bind(this);
        boundTimer();

    }

    async HandleWordInput(evt)
    {
        evt.preventDefault(evt);

        let messageType = 'notFound';
        const $wordInput = $("#wordInput");
        let word = $wordInput.val();

        if (this.foundWords.has(word))
        {
            this.showMessage(`You already found: ${word}`, messageType);
            return;
        }

        let queryObj = { word: word};
        const response = await axios.post("/ValidateWord", queryObj);
        let result = response.data.result;

        if (result === 'ok')
        {
            messageType = 'found';
            this.score += word.length;
            this.foundWords.add(word);
            $("#score").text(this.score);
            $("#foundWords").append($("<li>", { text: word }));
        }

        this.showMessage(result, messageType);
    }

    startGameTimer(){
        var timerInternal = async function() {
            this.counter = this.counter -1 ;                        

            if (this.counter < 0) {
                clearInterval(x);
                $("#WordForm").hide();
                this.showMessage(`Game over! - Your score is ${this.score}`, 'found');

                let queryObj = { score: this.score};
                const response = await axios.post("/Finish", queryObj);
            }
            else
            {
                this.showtimer(this.counter);
            }
            
        }

        // Update the count down every 1 second
        let x = setInterval(timerInternal.bind(this), 1000);
    }

    showtimer(ticks) {
        $("#timer").text(ticks);
    }

    showMessage(text, messageType) {
        $("#Message")
        .text(text)
        .removeClass()
        .addClass(messageType);
    }

}

let game = new BoggleGame();