$(document).ready(function () {
    $('#jquery-button').click(function (event) {
        alert("JQuery button click");
    })
    $('#color-test').hover(function () {
        $(this).css('color', 'red');
    },
    function () {
        $(this).css('color', 'black')
    })
});
