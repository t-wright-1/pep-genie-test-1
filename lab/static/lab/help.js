function help() {
    const helpDiv = document.getElementById('help-div');
    const helpIcon = document.getElementById('help-1');
    if (helpDiv.style.display == 'none') {
        helpDiv.style.display = 'flex';
        helpIcon.innerHTML = "X";
    } 
    else {
        helpDiv.style.display = 'none'
        helpIcon.innerHTML = "?";
    }
}