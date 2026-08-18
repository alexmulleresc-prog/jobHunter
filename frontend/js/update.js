const updateButton = document.getElementById("update-button");

function initializeUpdateButton(){
    updateButton.addEventListener("click",updateJobs);
}

async function updateJobs(){
    updateButton.disabled = true;
    updateButton.textContent = "⏳ Actualizando...";
    try{
        const result = await runScrapers();
        await loadDashboard();
        await loadJobs(currentFilters);
        if(result.new_jobs > 0){
            updateButton.textContent = `✅ +${result.new_jobs} nuevos`;
        }
        else
            {updateButton.textContent = "✔ Sin novedades";}
    }
    catch(error)
        {console.error(error);updateButton.textContent = "❌ Error";}
    await new Promise(resolve => setTimeout(resolve, 2000));
    updateButton.textContent = "Actualizar empleos";
    updateButton.disabled = false;
}