/* */
var bbuy_table = document.getElementById("bestbuy_table");
var popup_data = document.getElementById("fakepopup_data");

function displayInfo(){
  document.getElementById("fakepopup_data").style.display = "block";
  //popup_data.style.display = "block";
  console.log("revealingData");
}


function hideDisplayInfo(){
  document.getElementById("fakepopup_data").style.display = "none";
  console.log("hiding....");
}
