document.addEventListener('DOMContentLoaded', function() {
    const range_bars = document.querySelectorAll('.range-bar');
    const delete_buttons = document.querySelectorAll('.delete-button');

    
    // Handle for range bar and update button
    range_bars.forEach(range_bar => {
        range_bar.addEventListener('input', () => {
            const value = range_bar.value;
            const isbn = range_bar.parentElement.id;
            const current_process = document.querySelector(`#current-process-${isbn}`)
            range_bar.nextElementSibling.innerHTML = value;
            // Add listener to update button 
            range_bar.parentElement.nextElementSibling.addEventListener('click', () => {
                current_process.innerHTML = value;
                updateProcess(value, isbn);
            })
        })
    })

    // Handle for remove button
    delete_buttons.forEach(function(button) {
        button.addEventListener('click', () => {
            let del=confirm("Are you sure you want to delete this book from your reading list?");
            if(del) {
                const isbn = button.previousElementSibling.previousElementSibling.id;
                const book_item = document.getElementById(`book-${isbn}`);
                book_item.style.animationPlayState = 'running';
                book_item.addEventListener("animationend", () => {
                    book_item.remove()
                    removeMyReading(isbn);                   
                } )  
            }
        })
    })



    
})

// Process update function
function updateProcess(process, isbn) {
    fetch('update_process', {
        method: "PUT",
        body: JSON.stringify({
            process: process,
            isbn: isbn
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result)
    })
}


// Remove book from my reading fucntion
function removeMyReading(isbn) {
    fetch(`add_reading/${isbn}`,{
        method: 'POST'
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result)
    })
  }