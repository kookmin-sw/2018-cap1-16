        'use strict';

        
        (function(document, window, index) {
            // feature detection for drag&drop upload
            var isAdvancedUpload = function() {
                var div = document.createElement('div');
                return (('draggable' in div) || ('ondragstart' in div && 'ondrop' in div)) && 'FormData' in window && 'FileReader' in window;
            }();

                
            
            // applying the effect for every form
            var forms = document.querySelectorAll('#form_upload');
            Array.prototype.forEach.call(forms, function(form) {
                var input = form.querySelector('input[type="file"]'),
                    label = form.querySelector('#box_upload_filename'),
                    box = form.querySelector('.box_upload'),
                    errorMsg = form.querySelector('.box__error span'),
                    restart = form.querySelectorAll('.box__restart'),
                    droppedFiles = false, 
                    showFiles = function(files) {
                        label.textContent = files.length > 1 ? (input.getAttribute('data-multiple-caption') || '').replace('{count}', files.length) : files[0].name;
                    },
                    triggerFormSubmit = function() {
                        var event = document.createEvent('HTMLEvents');
                        event.initEvent('submit', true, false);
                        form.dispatchEvent(event);
                    };
                    console.log(form.getAttribute("method"));


                // letting the server side to know we are going to make an Ajax request
                // automatically submit the form on file select
                input.addEventListener('change', function(e) {
                    showFiles(e.target.files);
                    triggerFormSubmit();


                });
                // drag&drop files if the feature is available
                if (isAdvancedUpload) {
                    box.classList.add('has-advanced-upload'); // letting the CSS part to know drag&drop is supported by the browser

                    ['drag', 'dragstart', 'dragend', 'dragover', 'dragenter', 'dragleave', 'drop'].forEach(function(event) {
                        box.addEventListener(event, function(e) {
                            // preventing the unwanted behaviours
                            e.preventDefault();
                            e.stopPropagation();
                        });
                    });
                    ['dragover', 'dragenter'].forEach(function(event) {
                        box.addEventListener(event, function() {
                            box.classList.add('is-dragover');
                        });
                    });
                    ['dragleave', 'dragend', 'drop'].forEach(function(event) {
                        box.addEventListener(event, function() {
                            box.classList.remove('is-dragover');
                        });
                    });
                    box.addEventListener('drop', function(e) {
                        droppedFiles = e.dataTransfer.files; // the files that were dropped

                        //attach event handlers here...

                        //document.getElementById("file").value = ;
                        showFiles(droppedFiles);

                        triggerFormSubmit();

                    });
                }

                
                // if the form was submitted
                form.addEventListener('submit', function(e) {
                    var isLarge;
                    // preventing the duplicate submissions if the current one is in progress
                    if (form.classList.contains('is-uploading')) return false;

                    box.classList.add('is-uploading');
                    box.classList.remove('is-error');


                    if (isAdvancedUpload) // ajax file upload for modern browsers
                    {
                        e.preventDefault();
                        // gathering the form data
                        var ajaxData = new FormData(form);
                        
                        if (droppedFiles) {
                            Array.prototype.forEach.call(droppedFiles, function(file) {
                                if (file.size >= 33554432) {

                                    alert("Error, File is more than 32MB.");
                                    isLarge = false;
                                    location.href = "/upload/";
                                    return false;
                                } else {
                                    isLarge = true;
                                    ajaxData.append(input.getAttribute('name'), file);
                                    //alert(isLarge);
                                }
                            });


                        }

                        // ajax request
                        if(isLarge){ // startIF
                            var ajax = new XMLHttpRequest();
                            ajax.open(form.getAttribute('method'),form.getAttribute('action'), true);

                            ajax.onload = function() {
                                form.classList.remove('is-uploading');
                                var data = JSON.parse(ajax.responseText);
                                if ( parseInt(data.status) >= 200 && parseInt(data.status) < 400) {

                                    //form.classList.add(data.success == true ? 'is-success' : 'is-error');
                                    //if (!data.success) errorMsg.textContent = data.error;

                                    if( parseInt(data.analysis_type) == 0) {
                                        location.href = "/static_analysis/" + data.pk;
                                    }
                                    else if( parseInt(data.analysis_type) == 1){
                                        location.href = "/dynamic_analysis/" + data.pk;
                                    }


                                } else alert('Error. Please, contact the webmaster!');
                            }

                            ajax.onerror = function() {
                                form.classList.remove('is-uploading');
                                alert('Error. Please, try again!');
                            };

                            ajax.send(ajaxData);
                        
                        } //endIF
                    } else // fallback Ajax solution upload for older browsers
                    {
                        alert("old browsers");
                        var iframeName = 'uploadiframe' + new Date().getTime(),
                            iframe = document.createElement('iframe');

                        $iframe = $('<iframe name="' + iframeName + '" style="display: none;"></iframe>');

                        iframe.setAttribute('name', iframeName);
                        iframe.style.display = 'none';

                        document.body.appendChild(iframe);
                        form.setAttribute('target', iframeName);

                        iframe.addEventListener('load', function() {
                            var data = JSON.parse(iframe.contentDocument.body.innerHTML);
                            form.classList.remove('is-uploading')
                            form.classList.add(data.success == true ? 'is-success' : 'is-error')
                            form.removeAttribute('target');
                            if (!data.success) errorMsg.textContent = data.error;
                            iframe.parentNode.removeChild(iframe);
                        });
                    }

                });

           
                // restart the form if has a state of error/success
                Array.prototype.forEach.call(restart, function(entry) {
                    entry.addEventListener('click', function(e) {
                        e.preventDefault();
                        form.classList.remove('is-error', 'is-success');
                        input.click();
                    });
                });

            });
        }(document, window, 0));
