//Finally saves the selection in the correct order of the part ids and sets input HTML Tags accordingly
function saveSelection(){
    var table = document.getElementById("decision_table");
    var rows = table.rows;

    var sorted_selection =[];
    var sorted_weights = [];
    var sorted_value = [];
    var total_weight = 0;
    var total_value = 0;
    for(var i = 2; i < (rows.length - 3); i++){
        var part_id = parseInt(rows[i].getElementsByTagName("TD")[0].innerHTML);
        var weight = parseFloat(rows[i].getElementsByTagName("TD")[1].innerHTML);
        var value = parseFloat(rows[i].getElementsByTagName("TD")[2].innerHTML);
        var selected = document.getElementById('part_' + (part_id)).checked;
        total_weight += (weight*selected);
        total_value += (value*selected);
        sorted_weights[part_id-1] = weight;
        sorted_value[part_id-1] = value;
        sorted_selection[part_id-1] = selected; 
    }
    
    console.log(sorted_weights);
    console.log(sorted_value);
    console.log(sorted_selection);
    console.log('Total Weight: ' + total_weight);
    console.log('Total Value: ' + total_value);

    document.getElementById("id_r_weight").value = sorted_weights;
    document.getElementById("id_r_value").value = sorted_value;
    document.getElementById("id_sel").value = sorted_selection;
    document.getElementById("id_total_weight").value = total_weight;
    document.getElementById("id_total_value").value = total_value;
}
