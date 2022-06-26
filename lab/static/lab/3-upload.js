function showMock(){
    surface_box = document.getElementById('surface');
    surface_input = document.getElementById('surface-div');

    if (surface_box.checked == true) {
        surface_input.style.display = 'block';
    } else{
        surface_input.style.display = 'none';
    }

}


window.onload = showMock()
