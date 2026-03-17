document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('corrector-form');
    const submitBtn = document.getElementById('submit-btn');
    const btnText = submitBtn.querySelector('.btn-text');
    const spinner = submitBtn.querySelector('.spinner');
    
    const resultContainer = document.getElementById('result-container');
    const errorContainer = document.getElementById('error-container');
    
    const textoCorregidoEl = document.getElementById('texto-corregido');
    const explicacionEl = document.getElementById('explicacion');
    const errorMessageEl = document.getElementById('error-message');
    const copyBtn = document.getElementById('copy-btn');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // 1. Obtener valores del formulario
        const texto = document.getElementById('texto').value;
        const nivelCorreccion = document.getElementById('nivel_correccion').value;

        // 2. Estado de carga en la UI
        setLoadingState(true);
        hideElements([resultContainer, errorContainer]);

        try {
            // 3. Realizar la petición fetch() al backend
            const response = await fetch('/api/corregir', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    texto: texto,
                    nivel_correccion: nivelCorreccion
                })
            });

            const data = await response.json();

            // Verificar si el status de HTTP no es OK o si hay un "error" explícito en JSON
            if (!response.ok || data.error) {
                throw new Error(data.error || 'Error desconocido del servidor');
            }

            // 4. Procesar el resultado exitoso
            showResult(data.texto_corregido, data.explicacion);

        } catch (error) {
            // 5. Mostrar el error en la interfaz
            showError(error.message);
        } finally {
            // Restaurar estado del botón
            setLoadingState(false);
        }
    });

    // Funcionalidad para copiar el texto
    copyBtn.addEventListener('click', () => {
        const textToCopy = textoCorregidoEl.innerText;
        navigator.clipboard.writeText(textToCopy).then(() => {
            const originalIcon = copyBtn.innerHTML;
            // Show checkmark
            copyBtn.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>';
            setTimeout(() => {
                copyBtn.innerHTML = originalIcon;
            }, 2000);
        }).catch(err => {
            console.error('Error al copiar: ', err);
        });
    });

    // Helper functions for UI state
    function setLoadingState(isLoading) {
        if (isLoading) {
            btnText.classList.add('hidden');
            spinner.classList.remove('hidden');
            submitBtn.disabled = true;
            submitBtn.style.opacity = '0.7';
            submitBtn.style.cursor = 'not-allowed';
        } else {
            btnText.classList.remove('hidden');
            spinner.classList.add('hidden');
            submitBtn.disabled = false;
            submitBtn.style.opacity = '1';
            submitBtn.style.cursor = 'pointer';
        }
    }

    function showResult(texto, explicacion) {
        // En caso de que el JSON retorne undefined u otro valor anómalo
        textoCorregidoEl.textContent = texto || "No se recibió texto corregido.";
        explicacionEl.textContent = explicacion || "No hay explicaciones disponibles.";
        
        resultContainer.classList.remove('hidden');
        
        // Scroll suave hacia los resultados
        resultContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    function showError(message) {
        errorMessageEl.textContent = message;
        errorContainer.classList.remove('hidden');
    }

    function hideElements(elements) {
        elements.forEach(el => el.classList.add('hidden'));
    }
});
