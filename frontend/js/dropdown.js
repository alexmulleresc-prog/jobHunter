let activeDropdown = null;
let activeAnchor = null;

function showDropdown(anchor,items = [], onSelect = () => {}){
    closeDropdown();
    const dropdown = document.createElement("div");
    dropdown.className = "dropdown-menu";
    
    const rect = anchor.getBoundingClientRect();
    dropdown.style.top = `${rect.bottom + window.scrollY + 8}px`;
    dropdown.style.left = `${rect.left + window.scrollX}px`;
    
    items.forEach(item => {
        const option = document.createElement("div");
        option.className = "dropdown-item";
        option.textContent = `${item.name} (${item.count})`;;
        option.addEventListener("click",() => {onSelect(item);closeDropdown();});
        dropdown.appendChild(option);});

    document.body.appendChild(dropdown);
    setTimeout(() => {document.addEventListener("click", handleOutsideClick);}, 0);
    activeDropdown = dropdown;
    activeAnchor = anchor;
}

function closeDropdown() {
    if (!activeDropdown)return;
    activeDropdown.remove();
    activeDropdown = null;
     activeAnchor = null;
    document.removeEventListener("click", handleOutsideClick);
}

function handleOutsideClick(event){
    if(!activeDropdown) return;
    if(activeDropdown.contains(event.target) || activeAnchor.contains(event.target))
    return;
    closeDropdown();
    document.removeEventListener("click", handleOutsideClick);
}
