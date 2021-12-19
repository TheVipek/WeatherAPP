
function showDetails(){
    console.log('clicked');
    let div = document.querySelector(".additional_w_cont");
    if(div.classList.contains("show-display")){
        div.classList.remove("show-display");
    }else{
        div.classList.add("show-display");
    }
    // div.classList.toggle("not-display");
        // if (arrow.style.display == "none"){
    //     arrow.style.display = "grid";
    //     arrow.style.height = "100%";
    //     arrow.style.transition = "height 1s linear";
    // }else{
    //     arrow.style.height = "0%";
    //     arrow.style.display = "none";
    //     // arrow.style.transition = "min-height "
    // }
}