window.onload = function() {
    const nav_items = document.querySelectorAll('.nav-item');
    const hash = window.location.hash;
    
    if (nav_items.length == 3) { document.querySelector(".navbar-brand").style.marginRight = "30vw"; }  

    nav_items.forEach(item => {
        if(item == document.querySelector(hash+"-page"))
            set_active(item)
        
        item.addEventListener('click', () => {
            set_active(item);
            bg_animation();
        });
    });
    
    bg_animation(); 
}


window.onresize = function() { bg_animation(); }

// Imposta come attivo l'elemento selezionato
function set_active(item){
    document.querySelector(".nav-item.active").classList.remove("active")
    document.querySelector(".nav-link.active").classList.remove("active")
    
    item.classList.add("active")
    
    item.querySelector(".nav-link").classList.add("active")
}


// Muove lo sfondo dietro l'elemento selezionato
function bg_animation(){
    const movingBg = document.querySelector('.moving-bg');
    const rect = document.querySelector('.active').getBoundingClientRect();
    
    // Imposta la dimensione e la posizione dell'elemento "moving-bg"
    movingBg.style.width = `${rect.width}px`;
    movingBg.style.height = `${rect.height}px`;
    movingBg.style.left = `${rect.left}px`;
    movingBg.style.top = `${rect.top}px`;
}


