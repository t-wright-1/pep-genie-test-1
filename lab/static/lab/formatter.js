function showControl(){
    box = document.getElementById('normalisation_box');
    control_input = document.getElementById('control-div');

    if (box.checked == true) {
        control_input.style.display = 'block';
    } else{
        control_input.style.display = 'none';
    }

}

