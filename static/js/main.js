// --- Logic for the Main Page (home.html) ---
const homePageContent = document.querySelector('.main-content-grid');
if (homePageContent) {
    // 1. Sort Options Logic
    const sortButtons = document.querySelectorAll('.sort-options .sort-button');
    sortButtons.forEach(button => {
        button.addEventListener('click', function () {
            sortButtons.forEach(btn => btn.classList.remove('active-sort'));
            this.classList.add('active-sort');
        });
    });

    // 2. Pagination Logic
    // Logic removed: default link behavior is needed for server-side pagination.


    // 3. Filter Logic (Keywords and Checkboxes)
    const keywordsList = document.querySelector('.keywords-list');
    const checkboxes = document.querySelectorAll('.checkbox-group input[type="checkbox"]');

    if (keywordsList && checkboxes.length > 0) {
        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('change', function () {
                const keyword = this.dataset.keyword;
                if (this.checked) {
                    if (!document.querySelector(`.keyword-tag[data-keyword="${keyword}"]`)) {
                        const newTag = document.createElement('span');
                        newTag.className = 'keyword-tag';
                        newTag.setAttribute('data-keyword', keyword);
                        newTag.innerHTML = `${keyword} <i class="fa-solid fa-xmark remove-keyword-icon"></i>`;
                        keywordsList.appendChild(newTag);
                    }
                } else {
                    const tagToRemove = document.querySelector(`.keyword-tag[data-keyword="${keyword}"]`);
                    if (tagToRemove) {
                        tagToRemove.remove();
                    }
                }
            });
        });

        keywordsList.addEventListener('click', function (event) {
            const keywordIcon = event.target.closest('.remove-keyword-icon');
            if (keywordIcon) {
                const keywordTag = keywordIcon.closest('.keyword-tag');
                const keywordText = keywordTag.dataset.keyword;
                const checkbox = document.querySelector(`.checkbox-container input[data-keyword="${keywordText}"]`);
                if (checkbox) {
                    checkbox.checked = false;
                }
                keywordTag.remove();
            }
        });
    }
}

// --- Logic for Product Detail Pages (product-*.html) ---
const productPageContent = document.querySelector('.page-product');
if (productPageContent) {
    // Accordion
    const accordionTitle = document.querySelector('.accordion-title');
    if (accordionTitle) {
        accordionTitle.addEventListener('click', function () {
            this.closest('.accordion-item').classList.toggle('active');
        });
    }

    // Product Detail Page Quantity Logic
    const quantityContainer = document.querySelector('.quantity-controls');
    if (quantityContainer) {
        const minusBtn = quantityContainer.querySelector('.qty-btn-minus');
        const plusBtn = quantityContainer.querySelector('.qty-btn-plus');
        const qtyInput = quantityContainer.querySelector('.qty-input');

        if (minusBtn && plusBtn && qtyInput) {
            minusBtn.addEventListener('click', () => {
                let val = parseInt(qtyInput.value);
                if (val > parseInt(qtyInput.min || 1)) {
                    qtyInput.value = val - 1;
                }
            });

            plusBtn.addEventListener('click', () => {
                let val = parseInt(qtyInput.value);
                let max = parseInt(qtyInput.max);
                // If max is set, check it; otherwise just increment
                if (!max || val < max) {
                    qtyInput.value = val + 1;
                }
            });
        }
    }
}


// --- Logic for Account and Admin Pages ---
const accountAdminWrapper = document.querySelector('.account-page-wrapper, .admin-page-wrapper');
if (accountAdminWrapper) {
    // Account Page Tabs
    const accountTabs = document.querySelectorAll('.account-tab');
    const tabPanes = document.querySelectorAll('.tab-pane');

    if (accountTabs.length > 0 && tabPanes.length > 0) {
        accountTabs.forEach(tab => {
            tab.addEventListener('click', function () {
                accountTabs.forEach(item => item.classList.remove('active'));
                tabPanes.forEach(pane => pane.classList.remove('active'));
                const targetPane = document.querySelector(this.dataset.tabTarget);
                this.classList.add('active');
                if (targetPane) targetPane.classList.add('active');
            });
        });
    }

    // Admin Panel - Category Tags
    const categoryTagsContainer = document.querySelector('.category-tags');
    if (categoryTagsContainer) {
        categoryTagsContainer.addEventListener('click', function (e) {
            const clickedTag = e.target.closest('.category-tag');
            if (clickedTag) {
                categoryTagsContainer.querySelectorAll('.category-tag').forEach(t => t.classList.remove('active'));
                clickedTag.classList.add('active');
            }
        });
    }

    // Image Upload Simulation
    const uploadButton = document.getElementById('upload-image-btn');
    const fileInput = document.getElementById('image-upload-input');

    if (uploadButton && fileInput) {
        uploadButton.addEventListener('click', function () {
            fileInput.click();
        });

        fileInput.addEventListener('change', function (event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                const placeholder = document.querySelector('.image-upload-placeholder');

                reader.onload = function (e) {
                    placeholder.innerHTML = '';
                    placeholder.style.backgroundImage = `url('${e.target.result}')`;
                    placeholder.style.backgroundSize = 'cover';
                    placeholder.style.backgroundPosition = 'center';
                }
                reader.readAsDataURL(file);
            }
        });
    }
}