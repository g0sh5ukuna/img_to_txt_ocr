// Script pour améliorer l'expérience d'upload de fichiers avec prévisualisation

document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('file-upload-input');
    const uploadArea = document.getElementById('file-upload-area');
    const fileSelectedInfo = document.getElementById('file-selected-info');
    const fileName = document.getElementById('file-name');
    const fileSize = document.getElementById('file-size');
    const fileRemoveBtn = document.getElementById('file-remove-btn');
    const filePreview = document.getElementById('file-preview');
    const filePreviewImage = document.getElementById('file-preview-image');
    const filePreviewIcon = document.getElementById('file-preview-icon');
    const uploadForm = document.getElementById('upload-form');
    const submitBtn = document.getElementById('submit-btn');
    const btnText = submitBtn ? submitBtn.querySelector('.btn-text') : null;
    const btnLoader = submitBtn ? submitBtn.querySelector('.btn-loader') : null;

    if (!fileInput || !uploadArea) return;

    // Fonction pour formater la taille du fichier
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
    }

    // Fonction pour vérifier si le fichier est une image
    function isImageFile(file) {
        return file.type.startsWith('image/');
    }

    // Fonction pour vérifier si le fichier est un PDF
    function isPDFFile(file) {
        return file.type === 'application/pdf' || file.name.toLowerCase().endsWith('.pdf');
    }

    // Fonction pour créer une prévisualisation
    function createPreview(file) {
        if (!filePreview) return;

        // Cacher l'icône par défaut
        if (filePreviewIcon) {
            filePreviewIcon.style.display = 'none';
        }

        if (isImageFile(file)) {
            // Prévisualisation d'image
            const reader = new FileReader();
            reader.onload = function(e) {
                if (filePreviewImage) {
                    filePreviewImage.src = e.target.result;
                    filePreviewImage.style.display = 'block';
                }
            };
            reader.readAsDataURL(file);
        } else if (isPDFFile(file)) {
            // Pour les PDF, afficher une icône PDF
            if (filePreviewIcon) {
                filePreviewIcon.innerHTML = `
                    <svg width="64" height="64" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8L14 2Z" stroke="#dc3545" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M14 2V8H20" stroke="#dc3545" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M16 13H8" stroke="#dc3545" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M16 17H8" stroke="#dc3545" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M10 9H8" stroke="#dc3545" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    <span style="display: block; margin-top: 0.5rem; color: #dc3545; font-weight: 600;">PDF</span>
                `;
                filePreviewIcon.style.display = 'flex';
                filePreviewIcon.style.flexDirection = 'column';
                filePreviewIcon.style.alignItems = 'center';
            }
            if (filePreviewImage) {
                filePreviewImage.style.display = 'none';
            }
        } else {
            // Autres types de fichiers
            if (filePreviewIcon) {
                filePreviewIcon.innerHTML = `
                    <svg width="64" height="64" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8L14 2Z" stroke="#6c757d" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M14 2V8H20" stroke="#6c757d" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                `;
                filePreviewIcon.style.display = 'flex';
            }
            if (filePreviewImage) {
                filePreviewImage.style.display = 'none';
            }
        }
    }

    // Fonction pour afficher les informations du fichier sélectionné
    function showFileInfo(file) {
        fileName.textContent = file.name;
        fileSize.textContent = formatFileSize(file.size);
        fileSelectedInfo.style.display = 'block';
        uploadArea.style.display = 'none';
        
        // Créer la prévisualisation
        createPreview(file);
        
        // Afficher la zone de prévisualisation
        if (filePreview) {
            filePreview.style.display = 'block';
        }
    }

    // Fonction pour masquer les informations du fichier
    function hideFileInfo() {
        fileSelectedInfo.style.display = 'none';
        uploadArea.style.display = 'block';
        if (filePreview) {
            filePreview.style.display = 'none';
        }
        if (filePreviewImage) {
            filePreviewImage.src = '';
            filePreviewImage.style.display = 'none';
        }
        if (filePreviewIcon) {
            filePreviewIcon.style.display = 'none';
        }
        if (fileInput) {
            fileInput.value = '';
        }
    }

    // Gestion du changement de fichier
    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            showFileInfo(file);
        }
    });

    // Bouton pour supprimer le fichier sélectionné
    if (fileRemoveBtn) {
        fileRemoveBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            hideFileInfo();
        });
    }

    // Gestion du drag and drop
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        uploadArea.addEventListener(eventName, function() {
            uploadArea.classList.add('drag-over');
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, function() {
            uploadArea.classList.remove('drag-over');
        }, false);
    });

    uploadArea.addEventListener('drop', function(e) {
        const dt = e.dataTransfer;
        const files = dt.files;

        if (files.length > 0) {
            const file = files[0];
            // Créer un DataTransfer pour assigner le fichier
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            fileInput.files = dataTransfer.files;
            
            showFileInfo(file);
            
            // Déclencher l'événement change pour que le formulaire soit au courant
            const event = new Event('change', { bubbles: true });
            fileInput.dispatchEvent(event);
        }
    }, false);

    // Gestion de la soumission du formulaire
    if (uploadForm && submitBtn && btnText && btnLoader) {
        uploadForm.addEventListener('submit', function(e) {
            if (!fileInput.files || fileInput.files.length === 0) {
                e.preventDefault();
                alert('Veuillez sélectionner un fichier');
                return false;
            }

            // Afficher le loader
            btnText.style.display = 'none';
            btnLoader.style.display = 'flex';
            submitBtn.disabled = true;
        });
    }
});
