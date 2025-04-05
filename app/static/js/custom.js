/**
 * Hope Card - Custom JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    // Add page transition effect
    document.body.classList.add('fade-in');
    setTimeout(() => {
        document.body.classList.add('loaded');
    }, 300);

    // Mobile menu toggle with animation
    const menuToggle = document.getElementById('menuToggle');
    const navLinks = document.getElementById('navLinks');
    
    if (menuToggle && navLinks) {
        menuToggle.addEventListener('click', function() {
            navLinks.classList.toggle('active');
            
            // Animate burger menu
            this.classList.toggle('active');
            
            // Prevent scrolling when menu is open
            if (navLinks.classList.contains('active')) {
                document.body.style.overflow = 'hidden';
            } else {
                document.body.style.overflow = '';
            }
        });
    }

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                window.scrollTo({
                    top: target.offsetTop - 70,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Mouse trail effect
    const trailElements = 20;
    const trailElementsArray = [];
    
    for (let i = 0; i < trailElements; i++) {
        const trailElement = document.createElement('div');
        trailElement.className = 'mouse-trail';
        trailElement.style.opacity = (1 - i / trailElements);
        trailElement.style.width = (10 - i * 0.3) + 'px';
        trailElement.style.height = (10 - i * 0.3) + 'px';
        trailElement.style.zIndex = '9999';
        trailElement.style.position = 'fixed';
        trailElement.style.borderRadius = '50%';
        trailElement.style.pointerEvents = 'none';
        trailElement.style.background = 'rgba(59, 130, 246, 0.5)';
        trailElement.style.transition = 'width 0.2s, height 0.2s, opacity 0.5s';
        document.body.appendChild(trailElement);
        trailElementsArray.push({ element: trailElement, x: 0, y: 0 });
    }
    
    window.addEventListener('mousemove', e => {
        trailElementsArray[0].x = e.clientX;
        trailElementsArray[0].y = e.clientY;
    });
    
    function updateTrail() {
        let x = trailElementsArray[0].x;
        let y = trailElementsArray[0].y;
        
        for (let i = 0; i < trailElementsArray.length; i++) {
            const currentElement = trailElementsArray[i];
            const nextElement = trailElementsArray[i + 1];
            
            currentElement.element.style.left = x + 'px';
            currentElement.element.style.top = y + 'px';
            
            if (nextElement) {
                nextElement.x = x + (nextElement.x - x) * 0.8;
                nextElement.y = y + (nextElement.y - y) * 0.8;
                x = nextElement.x;
                y = nextElement.y;
            }
        }
        
        requestAnimationFrame(updateTrail);
    }
    
    updateTrail();

    // Enhanced auto-close alerts with progress bar
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        if (alert.classList.contains('auto-close') || !alert.classList.contains('persistent')) {
            // Add progress bar
            const progressBar = document.createElement('div');
            progressBar.className = 'alert-progress';
            progressBar.style.cssText = 'position: absolute; bottom: 0; left: 0; height: 3px; background: rgba(255,255,255,0.5); width: 100%; transform-origin: left';
            alert.style.position = 'relative';
            alert.appendChild(progressBar);
            
            // Animate progress bar
            progressBar.animate(
                [
                    { transform: 'scaleX(1)' },
                    { transform: 'scaleX(0)' }
                ],
                {
                    duration: 5000,
                    easing: 'linear',
                    fill: 'forwards'
                }
            );
            
            setTimeout(() => {
                alert.style.opacity = '0';
                alert.style.transform = 'translateY(-20px)';
                alert.style.transition = 'opacity 0.3s, transform 0.3s';
                setTimeout(() => {
                    alert.remove();
                }, 300);
            }, 5000);
        }
        
        // Add close button
        if (!alert.querySelector('.alert-close')) {
            const closeBtn = document.createElement('button');
            closeBtn.className = 'alert-close';
            closeBtn.innerHTML = '&times;';
            closeBtn.style.cssText = 'position: absolute; top: 10px; left: 10px; background: none; border: none; color: inherit; font-size: 1.2rem; cursor: pointer; opacity: 0.7';
            closeBtn.addEventListener('click', () => {
                alert.style.opacity = '0';
                alert.style.transform = 'translateY(-20px)';
                alert.style.transition = 'opacity 0.3s, transform 0.3s';
                setTimeout(() => {
                    alert.remove();
                }, 300);
            });
            alert.appendChild(closeBtn);
        }
    });

    // Add automatic dark/light mode based on user's system preference
    const prefersDarkMode = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (prefersDarkMode) {
        document.body.classList.add('dark-mode');
    }
    
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', event => {
        if (event.matches) {
            document.body.classList.add('dark-mode');
        } else {
            document.body.classList.remove('dark-mode');
        }
    });

    // Enhanced form validation with animations
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        // Real-time validation
        const requiredFields = form.querySelectorAll('[required]');
        requiredFields.forEach(field => {
            field.addEventListener('blur', function() {
                validateField(field);
            });
            
            field.addEventListener('input', function() {
                if (field.classList.contains('invalid')) {
                    validateField(field);
                }
            });
        });
        
        form.addEventListener('submit', function(e) {
            let isValid = true;

            requiredFields.forEach(field => {
                if (!validateField(field)) {
                    isValid = false;
                }
            });

            if (!isValid) {
                e.preventDefault();
                
                // Scroll to first error
                const firstError = form.querySelector('.invalid');
                if (firstError) {
                    firstError.focus();
                    firstError.scrollIntoView({
                        behavior: 'smooth',
                        block: 'center'
                    });
                }
                
                // Shake form on error
                form.animate(
                    [
                        { transform: 'translateX(0)' },
                        { transform: 'translateX(-10px)' },
                        { transform: 'translateX(10px)' },
                        { transform: 'translateX(-10px)' },
                        { transform: 'translateX(0)' }
                    ],
                    {
                        duration: 400,
                        easing: 'ease-in-out'
                    }
                );
            }
        });
    });
    
    function validateField(field) {
        const isValid = field.value.trim() !== '';
        if (!isValid) {
            field.classList.add('invalid');
            field.classList.remove('valid');
            
            // Show validation message
            let validationMessage = field.nextElementSibling;
            if (!validationMessage || !validationMessage.classList.contains('validation-message')) {
                validationMessage = document.createElement('div');
                validationMessage.className = 'validation-message text-danger';
                validationMessage.style.cssText = 'font-size: 0.8rem; margin-top: 0.25rem; transform: translateY(-5px); opacity: 0; transition: all 0.3s';
                field.parentNode.insertBefore(validationMessage, field.nextSibling);
                
                // Animate in
                setTimeout(() => {
                    validationMessage.style.transform = 'translateY(0)';
                    validationMessage.style.opacity = '1';
                }, 10);
            }
            validationMessage.textContent = 'هذا الحقل مطلوب';
            
        } else {
            field.classList.remove('invalid');
            field.classList.add('valid');
            
            // Remove validation message
            const validationMessage = field.nextElementSibling;
            if (validationMessage && validationMessage.classList.contains('validation-message')) {
                validationMessage.style.transform = 'translateY(-5px)';
                validationMessage.style.opacity = '0';
                setTimeout(() => {
                    validationMessage.remove();
                }, 300);
            }
        }
        return isValid;
    }

    // Add parallax effect to hero sections
    const heroSection = document.querySelector('.hero-section');
    if (heroSection) {
        window.addEventListener('scroll', () => {
            const scrollPosition = window.scrollY;
            if (scrollPosition < window.innerHeight) {
                heroSection.style.backgroundPositionY = scrollPosition * 0.5 + 'px';
                
                // Parallax for hero content
                const heroContent = heroSection.querySelector('.hero-content');
                if (heroContent) {
                    heroContent.style.transform = `translateY(${scrollPosition * 0.2}px)`;
                }
            }
        });
    }

    // Animated counter for stats
    const statNumbers = document.querySelectorAll('[data-count]');
    
    if (statNumbers.length > 0) {
        const animateCounter = (el) => {
            const target = parseInt(el.dataset.count);
            const duration = 2000; // ms
            const start = 0;
            const increment = target / (duration / 16);
            
            let current = start;
            const timer = setInterval(() => {
                current += increment;
                if (current >= target) {
                    el.textContent = target.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") + "+";
                    clearInterval(timer);
                } else {
                    el.textContent = Math.floor(current).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") + "+";
                }
            }, 16);
        };
        
        // Use Intersection Observer to animate when visible
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateCounter(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });
        
        statNumbers.forEach(stat => {
            observer.observe(stat);
        });
    }

    // Handle tags input with animation
    const tagsInputs = document.querySelectorAll('.tags-input');
    tagsInputs.forEach(input => {
        const tagsContainer = document.createElement('div');
        tagsContainer.className = 'tags-container';
        tagsContainer.style.display = 'flex';
        tagsContainer.style.flexWrap = 'wrap';
        tagsContainer.style.gap = '0.5rem';
        tagsContainer.style.marginTop = '0.5rem';
        input.parentNode.insertBefore(tagsContainer, input.nextSibling);
        
        const hiddenContainer = document.createElement('div');
        hiddenContainer.className = 'hidden-inputs';
        hiddenContainer.style.display = 'none';
        input.parentNode.appendChild(hiddenContainer);
        
        function renderTags() {
            const tags = input.value.split(',').filter(tag => tag.trim() !== '');
            
            tagsContainer.innerHTML = '';
            hiddenContainer.innerHTML = '';
            
            tags.forEach((tag, index) => {
                const tagEl = document.createElement('span');
                tagEl.className = 'badge badge-primary me-1 mb-1';
                tagEl.style.cssText = 'display: inline-flex; align-items: center; padding: 0.4rem 0.8rem; border-radius: 50px; opacity: 0; transform: scale(0.8); transition: all 0.3s;';
                tagEl.textContent = tag.trim();
                
                const removeBtn = document.createElement('span');
                removeBtn.className = 'tag-remove ms-1';
                removeBtn.innerHTML = '&times;';
                removeBtn.style.cssText = 'cursor: pointer; margin-right: 0.25rem; font-size: 1.2rem; line-height: 1;';
                removeBtn.addEventListener('click', () => {
                    // Animate out
                    tagEl.style.opacity = '0';
                    tagEl.style.transform = 'scale(0.8)';
                    setTimeout(() => {
                        const newTags = tags.filter((_, i) => i !== index);
                        input.value = newTags.join(',');
                        renderTags();
                    }, 300);
                });
                
                tagEl.appendChild(removeBtn);
                tagsContainer.appendChild(tagEl);
                
                // Animate in
                setTimeout(() => {
                    tagEl.style.opacity = '1';
                    tagEl.style.transform = 'scale(1)';
                }, 50 * index);
                
                // Add hidden input for form submission
                const hiddenInput = document.createElement('input');
                hiddenInput.type = 'hidden';
                hiddenInput.name = input.dataset.fieldName || input.name;
                hiddenInput.value = tag.trim();
                hiddenContainer.appendChild(hiddenInput);
            });
        }
        
        input.addEventListener('keydown', e => {
            if (e.key === 'Enter' || e.key === ',') {
                e.preventDefault();
                renderTags();
            }
        });
        
        input.addEventListener('blur', renderTags);
        
        // Initial render
        renderTags();
    });

    // Enhanced table search functionality
    const tableSearchInputs = document.querySelectorAll('.table-search');
    tableSearchInputs.forEach(input => {
        const tableId = input.dataset.tableTarget;
        const table = document.getElementById(tableId);
        
        if (table) {
            const rows = table.querySelectorAll('tbody tr');
            
            // Add search icon
            const searchIcon = document.createElement('span');
            searchIcon.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>';
            searchIcon.style.cssText = 'position: absolute; left: 10px; top: 50%; transform: translateY(-50%); opacity: 0.5;';
            
            // Style the input
            input.style.paddingLeft = '35px';
            input.parentNode.style.position = 'relative';
            input.parentNode.insertBefore(searchIcon, input);
            
            // Add clear button
            const clearBtn = document.createElement('button');
            clearBtn.type = 'button';
            clearBtn.innerHTML = '&times;';
            clearBtn.style.cssText = 'position: absolute; left: 35px; top: 50%; transform: translateY(-50%); background: none; border: none; cursor: pointer; opacity: 0; transition: opacity 0.3s; font-size: 1.2rem; line-height: 1; color: #666;';
            input.parentNode.insertBefore(clearBtn, input.nextSibling);
            
            // Toggle clear button visibility
            input.addEventListener('input', () => {
                const searchTerm = input.value.toLowerCase();
                clearBtn.style.opacity = searchTerm ? '0.5' : '0';
                
                rows.forEach(row => {
                    const text = row.textContent.toLowerCase();
                    if (text.includes(searchTerm)) {
                        row.style.display = '';
                    } else {
                        row.style.display = 'none';
                    }
                });
                
                // Show empty state if no results
                let noResultsMsg = table.nextElementSibling;
                if (!noResultsMsg || !noResultsMsg.classList.contains('no-results')) {
                    noResultsMsg = document.createElement('div');
                    noResultsMsg.className = 'no-results text-center py-4';
                    noResultsMsg.innerHTML = 'لا توجد نتائج مطابقة للبحث';
                    noResultsMsg.style.display = 'none';
                    table.parentNode.insertBefore(noResultsMsg, table.nextSibling);
                }
                
                const hasVisibleRows = Array.from(rows).some(row => row.style.display !== 'none');
                noResultsMsg.style.display = hasVisibleRows ? 'none' : 'block';
            });
            
            // Clear search
            clearBtn.addEventListener('click', () => {
                input.value = '';
                input.dispatchEvent(new Event('input'));
                input.focus();
            });
        }
    });

    // Enhanced print functionality
    const printButtons = document.querySelectorAll('.print-btn');
    printButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Add print animation
            button.classList.add('printing');
            
            // Add print timestamp
            const timestamp = document.createElement('div');
            timestamp.className = 'print-timestamp';
            timestamp.innerHTML = 'تم الطباعة في: ' + new Date().toLocaleString('ar');
            timestamp.style.cssText = 'text-align: center; margin-bottom: 1rem; font-size: 0.8rem; color: #666;';
            
            // Find the content to print
            const printTarget = button.dataset.printTarget ? 
                document.querySelector(button.dataset.printTarget) : 
                button.closest('.card, .container');
                
            if (printTarget) {
                printTarget.prepend(timestamp.cloneNode(true));
            }
            
            setTimeout(() => {
                window.print();
                
                // Remove timestamp after printing
                const addedTimestamp = document.querySelector('.print-timestamp');
                if (addedTimestamp) {
                    addedTimestamp.remove();
                }
                
                // Remove animation class
                setTimeout(() => {
                    button.classList.remove('printing');
                }, 500);
            }, 300);
        });
    });
    
    // Add ripple effect to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            ripple.classList.add('ripple');
            this.appendChild(ripple);
            
            const rect = button.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            
            ripple.style.width = ripple.style.height = `${size}px`;
            ripple.style.left = `${e.clientX - rect.left - size / 2}px`;
            ripple.style.top = `${e.clientY - rect.top - size / 2}px`;
            
            ripple.classList.add('active');
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
}); 