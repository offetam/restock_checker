/* */
var bbuy_table = document.getElementById("bestbuy_table");
var popup_data = document.getElementById("fakepopup_data");

function displayInfo(product_id, productName, bestbuyData){
  console.log(product_id)
  document.getElementById("fakepopup_data").style.display = "block";
  document.getElementById("fakepopup_data_main").value = product_id;
  console.log("New value: " + document.getElementById("fakepopup_data_main").value);
  document.getElementById("fakepopup_data_main").innerHTML = productName;
  // {% for x in all_enteries %}
  // // console.log("values to be added.")
  // {% endfor %}

//  console.log("revealingData");
}


function hideDisplayInfo(){
  document.getElementById("fakepopup_data").style.display = "none";
  //console.log("hiding....");
}
