quote()

function quote() {
    const api_url ="https://type.fit/api/quotes";
    
        fetch(api_url)
        .then(response => response.json())
        .then(result => {
            // Print result
            const randomQuote = result[Math.floor(Math.random() * result.length)];
            console.log(randomQuote)
            const text = randomQuote['text'];
            const author = randomQuote['author'] !== null ? randomQuote['author'] : "Anonymous";
            document.querySelector('.blockquote').innerHTML = `<p>${text}</p>`
            document.querySelector('.blockquote-footer').innerHTML = `<cite title="Source Title">${author}</cite>`
        })
        
}


setInterval( quote , 10000);