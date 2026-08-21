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

function initializeSort(){
    const jobsCard = document.getElementById("jobs-card");
    jobsCard.addEventListener("click", () => {
        const options = [
            { name: "Más recientes", value: "recientes" },
            { name: "Más antiguos", value: "antiguos" },
            { name: "Título A → Z", value: "titulo_az" },
            { name: "Título Z → A", value: "titulo_za" },
            { name: "Empresa A → Z", value: "empresa_az" },
            { name: "Empresa Z → A", value: "empresa_za" }
        ];
        closeDropdown();
        const dropdown = document.createElement("div");
        dropdown.className = "dropdown-menu";
        const rect = jobsCard.getBoundingClientRect();
        dropdown.style.top =
            `${rect.bottom + window.scrollY + 8}px`;
        dropdown.style.left =
            `${rect.left + window.scrollX}px`;
        options.forEach(option => {
            const item = document.createElement("div");
            item.className = "dropdown-item";
            item.textContent = option.name;
            item.addEventListener("click", async (event) => {
                event.stopPropagation();
                currentOrder = option.value;
                currentPage = 1;
                closeDropdown();
                await loadJobs(currentFilters);
            });
            dropdown.appendChild(item);
        });
        document.body.appendChild(dropdown);
        activeDropdown = dropdown;
        activeAnchor = jobsCard;
        setTimeout(() => {
            document.addEventListener("click", handleOutsideClick);
        }, 0);
    });
}
