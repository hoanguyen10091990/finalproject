document.addEventListener('DOMContentLoaded', function() {

    // Handle for display star in rating 
    const ratings = document.querySelectorAll('.rating');
    ratings.forEach(rating => {
        rate = rating.innerHTML.substring(7).trim();
        if (rating != "None") {
            rating.innerHTML = "Rating: " + getStars(Number(rate));           
        } 
    })

    // Handle for delete review 
    const delete_buttons = document.querySelectorAll('.delete-button');
    delete_buttons.forEach(button => {
        button.addEventListener('click', function () {
            let del=confirm("Are you sure you want to delete this review?");
            if (del) {
                const review_id = Number(button.parentElement.id);
                button.parentElement.style.animationPlayState = 'running';
                button.parentElement.addEventListener('animationend', () => {
                    button.parentElement.remove();
                    deleteReview(review_id);
                })
            }
        })
    })
})

function getStars(rating) {

    // Round to nearest half
    rating = Math.round(rating * 2) / 2;
    let output = [];
  
    // Append all the filled whole stars
    for (var i = rating; i >= 1; i--)
      output.push('<i class="bi bi-star-fill" aria-hidden="true" style="color: gold;"></i>&nbsp;');
  
    // If there is a half a star, append it
    if (i == .5) output.push('<i class="bi bi-star-half" aria-hidden="true" style="color: gold;"></i>&nbsp;');
  
    // Fill the empty stars
    for (let i = (5 - rating); i >= 1; i--)
      output.push('<i class="bi bi-star" aria-hidden="true" style="color: gold;"></i>&nbsp;');
  
    return output.join('');
  
  }


function deleteReview(id) {
    fetch(`delete/${id}`,{
        method: 'PUT'
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result)
    })
  }



  