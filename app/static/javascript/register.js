function Matcher(x , y) {
    first = document.getElementById(x).value;
    second = document.getElementById(y).value;
    if(first == second){
        return true;
    }else{
        text = document.getElementById("confirmation");
        text.innerHTML = 'something went wrong';
        return false;
    }
}

Matcher("password","re-password");
Matcher("email","re-email");