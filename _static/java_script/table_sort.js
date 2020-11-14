//INITIAL SORT
//1 = Ascending | 0 = Not sorted | -1 = Descending
var current_sort = [1, 0, 0, 0]; //Initially the parts are sorted by ther ID
var arrow_header = [];


//Set the arrow header with the correct arrows according to the current_sort array
function setSortSymbols(current_sort){

    arrow_header = Array.from(current_sort);
    
    for(var i = 0; i < arrow_header.length; i++){
        if(arrow_header[i] == 0){
            arrow_header[i] = ' <span style="color:grey">&#11206&#11205</span>';
        }else if(arrow_header[i] == -1){     //Descending
            arrow_header[i] = ' &#11206';     //Arrow DOWN
        }else if(arrow_header[i] == 1){      //Ascending
            arrow_header[i] = ' &#11205';     //Arrow UP
        }
    }            
}

//Update the Table Headings with the correct sorting symbols
function updateHeadings(){
    $('#arrow_part').html(arrow_header[0]);
    $('#arrow_weight').html(arrow_header[1]);
    $('#arrow_prob').html(arrow_header[2]);
    $('#arrow_ratio').html(arrow_header[3]);
}

//Function to sort the table according to the current_sort array
function sortTable(current_sort) {
    
    //Get Column and Order
    var column, order;
    for(var i = 0; i < current_sort.length; i++){
        if(current_sort[i] != 0){
            column = i;
            order = current_sort[i];
            break;
        }
    }

    var table, rows, switching, i, x, y, shouldSwitch;
    table = document.getElementById("decision_table");
    switching = true;
    /*Make a loop that will continue until no switching has been done:*/
    // console.log(table);
    
    while (switching) {
        //start by saying: no switching is done:
        switching = false;
        rows = table.rows;
        /*Loop through all table rows (except the first, which contains table headers):*/
        for (i = 2; i < (rows.length - 4); i++) {
            //start by saying there should be no switching:
            shouldSwitch = false;
            /*Get the two elements you want to compare, one from current row and one from the next:*/
            x = parseFloat(rows[i].getElementsByTagName("TD")[column].innerHTML);
            y = parseFloat(rows[i + 1].getElementsByTagName("TD")[column].innerHTML);
            // console.log(typeof x);
            // console.log('Compare ' + x + ' to ' + y);

            //check if the two rows should switch place:
            
            if(order == -1 && x < y) { //Descending
                //if so, mark as a switch and break the loop:
                // console.log('Since ' + x + ' > ' + y + ' switch ' + x + ' and ' + y + '----------------------------');
                shouldSwitch = true;
                break;
            }
            if(order == 1 && x > y){ //Ascending
                //if so, mark as a switch and break the loop:
                // console.log('Since ' + x + ' > ' + y + ' switch ' + x + ' and ' + y + '----------------------------');
                shouldSwitch = true;
                break;
            }
        }
        if (shouldSwitch) {
            /*If a switch has been marked, make the switch and mark that a switch has been done:*/
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
        }
    }
}

//When the window is loaded we assign the onclick functions
$(function(){
    setSortSymbols(current_sort); //Ascending, Column 0 (PartID), 4 Columns
    updateHeadings();
    assignOnClicks();
});

//Assign onClick Functions
function assignOnClicks(){
    $("#sort_id").click(function(){
        sort_main(0);
    });
    $("#sort_w").click(function(){
        sort_main(1);
    });
    $("#sort_p").click(function(){
        sort_main(2);
    });
    $("#sort_r").click(function(){
        sort_main(3);
    });          
}

//Function that rearranges the current_sort array according to the last click and starts sortTable(), setSortSymbols() and the Headings
function sort_main(column){
    for(var i = 0; i < current_sort.length; i++){
        if (i == column){
            if(current_sort[i] == 1){
                current_sort[i] = -1;
            }else{
                current_sort[i] = 1
            }
        }else{
            current_sort[i]=0;
        }
    }
    console.log(current_sort);
    sortTable(current_sort);
    setSortSymbols(current_sort);
    updateHeadings();
}