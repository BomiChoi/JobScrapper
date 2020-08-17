var sw = true

function loading(){
    $('.loading').text("Searching...")
    setInterval("changeText()", 3000);
}

function changeText(){
    txt = $('.loading')
    if(sw) {
        txt.text("It may take some time...")
        sw = false
    } else {
        txt.text("Searching...")
        sw = true
    }
}
