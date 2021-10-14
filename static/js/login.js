/* Functions to hide/unhide forms*/
function unhide_account(){
    document.getElementById("login_form").style.display = "none";
    document.getElementById("account_form").style.display = "block";
    console.log("entered this section.");
}

function unhide_login(){
  document.getElementById("login_form").style.display = "block";
  document.getElementById("account_form").style.display = "none";
  console.log("entered this section.");
}
