window.onload = function() {
    const nav_items = document.querySelectorAll('.nav-item');
    var hash = window.location.hash;

    if (!hash)
        hash = '#home';
    
    if (nav_items.length == 3) { document.querySelector(".navbar-brand").style.marginRight = "30vw"; }  
    
    nav_items.forEach(item => {
        if(hash){
            if(item == document.querySelector(hash))
                set_active(item)
        }
        
        item.addEventListener('click', () => {
            set_active(item);
            bg_animation();
        });
    });
    
    remove_hash();
    bg_animation();
}


window.onresize = function() { bg_animation(); }

window.onhashchange = function() { bg_animation(); }

window.addEventListener("popstate", function() { 
    remove_hash();
    bg_animation(); 
});

function remove_hash(){
    if( window.location.pathname.includes('/signup/') ||
        window.location.pathname.includes('/recipe/') || 
        window.location.pathname.includes('/user/')){
        
        const new_url = window.location.href.replace(/#.*$/, '');
        window.history.replaceState(null, null, new_url);
    }
}

function set_active(item){
    document.querySelector(".nav-item.active").classList.remove("active")
    document.querySelector(".nav-link.active").classList.remove("active")
    
    item.classList.add("active")
    
    item.querySelector(".nav-link").classList.add("active")
}

function bg_animation(){
    if( window.location.pathname.includes('/signup/') ||
        window.location.pathname.includes('/recipe/') || 
        window.location.pathname.includes('/user/'))
        
        return;

    const movingBg = document.querySelector('.moving-bg');
    const rect = document.querySelector('.active').getBoundingClientRect();
    
    movingBg.style.width = `${rect.width}px`;
    movingBg.style.height = `${rect.height}px`;
    movingBg.style.left = `${rect.left}px`;
    movingBg.style.top = `${rect.top}px`;
}


