function showLoaderOnClick(url) {
    showLoader();
}
function showLoader(){
    $('body').append('<div style="" id="loadingDiv"><div class="loader">Loading...</div></div>');
}