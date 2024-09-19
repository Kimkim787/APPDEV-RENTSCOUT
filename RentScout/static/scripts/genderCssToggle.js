const selectElement = document.getElementById('gender');
                    let isOptionsOpen = false;
                
                    selectElement.addEventListener('mousedown', function(e) {
                        if (!isOptionsOpen) {
                            selectElement.style.borderBottomLeftRadius = '0';
                            selectElement.style.borderBottomRightRadius = '0';
                            isOptionsOpen = true;
                        } else {
                            selectElement.style.borderBottomLeftRadius = '';
                            selectElement.style.borderBottomRightRadius = '';
                            isOptionsOpen = false;
                        }
                    });
                
                    selectElement.addEventListener('blur', function() {
                        selectElement.style.borderBottomLeftRadius = '';
                        selectElement.style.borderBottomRightRadius = '';
                        isOptionsOpen = false;
                    });