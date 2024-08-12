function change_active(element){
    console.log(element)
    
    console.log(document.getElementsByClassName("nav-item active"))
    document.getElementsByClassName("nav-item active")[0].classList.remove("active")
    document.getElementsByClassName("nav-link active")[0].classList.remove("active")
    
    element.classList.add("active")
    
    for (var child of element.children){
        if(child.classList[0] == "nav-link")
            child.classList.add("active")
    }

}