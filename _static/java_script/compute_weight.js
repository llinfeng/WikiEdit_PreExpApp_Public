//When the window is loaded we assign the onclick functions
$(function(){
    computeWeight();
    $(".gurke").click(function(){
        computeWeight();
    })
    
});

//Computes the weight of the current selection and sets error message if capacity is exceeded
function computeWeight(){
    var table = document.getElementById("decision_table");
    var rows = table.rows;
    
    var totalWeight = 0;
    var totalValue = 0;
    
    for(var i = 2; i < (rows.length - 3); i++){
        var part_id = parseInt(rows[i].getElementsByTagName("TD")[0].innerHTML);
        var c_weight = parseFloat(rows[i].getElementsByTagName("TD")[1].innerHTML);
        var c_value = parseFloat(rows[i].getElementsByTagName("TD")[2].innerHTML);
        var selected = document.getElementById('part_' + (part_id)).checked;
        totalWeight += (c_weight*selected);  
        totalValue += (c_value*selected);
    }
    $('#total_weight').html(totalWeight);
    $('#total_value').html(totalValue);
    try {
        if(totalWeight>capacity){
            $('#message').html('<div class="alert alert-danger" role="alert"> Your selection weighs <b>' + (totalWeight-capacity) + ' lb</b> more than you have capacity! Please select fewer items! </div>');
            document.getElementById("Next_Button").disabled = true;
        }else{
            $('#message').html('<br><br>');
            document.getElementById("Next_Button").disabled = false;
        }
      }
      catch(error) {
        console.error(error);
        // expected output: ReferenceError: nonExistentFunction is not defined
        // Note - error messages will vary depending on browser
      }
    

}