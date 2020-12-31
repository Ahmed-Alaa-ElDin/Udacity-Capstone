$(function() {
    console.log($('#movie-actor'));
    $('#movie-actor').chosen();
    $('#movie-actor').change(function() {
        console.log($('#movie-actor').val());
    })
})