function showMenu(){
    const navUl = document.getElementById('nav-ul');

    if (navUl.className === "nav-ul") {
        navUl.className += " responsive";
    } else {
        navUl.className = "nav-ul";
    }
    
}