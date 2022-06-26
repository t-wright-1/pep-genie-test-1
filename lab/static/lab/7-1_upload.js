function showMock(){
    mock_box = document.getElementById('auto_mock');
    mock_input = document.getElementById('mock-div');

    if (mock_box.checked == true) {
        mock_input.style.display = 'block';
    } else{
        mock_input.style.display = 'none';
    }

}


window.onload = showMock()
