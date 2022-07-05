const initialRating = $('#id_rating').val();
if(initialRating==5){
    $('#5, #4, #3, #2, #1').html(`&#9733;`)
} else if(initialRating==4){
    $('#4, #3, #2, #1').html(`&#9733;`)
} else if(initialRating==3){
    $('#3, #2, #1').html(`&#9733;`)
} else if(initialRating==2){
    $('#2, #1').html(`&#9733;`)
} else if(initialRating==1){
    $('#1').html(`&#9733;`)
};

$('.star').on('click', function(event){
    rating.value = event.target.id
});

var rating = document.getElementById('id_rating');

$('#5').on('mouseover click', ()=>{
    $('#1, #2, #3, #4, #5').html(`&#9733;`)
});
$('#4').on('mouseover click', ()=>{
    $('#1, #2, #3, #4').html(`&#9733;`);
    $('#5').html(`&#9734;`);
});
$('#3').on('mouseover click', ()=>{
    $('#1, #2, #3').html(`&#9733;`);
    $('#4, #5').html(`&#9734;`);
});
$('#2').on('mouseover click', ()=>{
    $('#1, #2').html(`&#9733;`);
    $('#3, #4, #5').html(`&#9734;`);
});
$('#1').on('mouseover click', ()=>{
    $('#1').html(`&#9733;`);
    $('#2, #3, #4, #5').html(`&#9734;`);
});