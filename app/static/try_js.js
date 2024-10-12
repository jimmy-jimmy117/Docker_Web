function change_table(){
    table_obj = document.getElementById('table_id');
    if (color === "red") {
        color = "";
    } else {
        color = "red";
    }
    table_obj.style.backgroundColor = color;
}

var color = "";