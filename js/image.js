// 图片处理功能
function initImageFunctions() {
    const imageUpload = document.getElementById('image-upload');
    const imageList = document.getElementById('image-list');
    const widthInput = document.getElementById('width');
    const heightInput = document.getElementById('height');
    const maintainRatio = document.getElementById('maintain-ratio');
    const rotateLeft = document.getElementById('rotate-left');
    const rotateRight = document.getElementById('rotate-right');
    const watermarkText = document.getElementById('watermark-text');
    const watermarkColor = document.getElementById('watermark-color');
    const watermarkOpacity = document.getElementById('watermark-opacity');
    const compressionQuality = document.getElementById('compression-quality');
    const previewBtn = document.querySelector('#image-process .btn-preview');
    const processBtn = document.querySelector('#image-process .btn-process');
    const imagePreview = document.querySelector('#image-process .preview-content');
    
    // 存储上传的图片
    const uploadedImages = [];
    let currentRotation = 0;
    
    // 图片上传处理
    if (imageUpload) {
        imageUpload.addEventListener('change', (e) => {
            const files = e.target.files;
            if (files.length > 0) {
                imageList.innerHTML = '';
                uploadedImages.length = 0;
                
                for (let i = 0; i < files.length; i++) {
                    const file = files[i];
                    const reader = new FileReader();
                    
                    reader.onload = function(e) {
                        const img = new Image();
                        img.onload = function() {
                            // 存储图片信息
                            uploadedImages.push({
                                name: file.name,
                                width: img.width,
                                height: img.height,
                                original: img
                            });
                            
                            // 创建图片列表项
                            const imageItem = document.createElement('div');
                            imageItem.className = 'image-item';
                            imageItem.innerHTML = `
                                <div class="image-thumbnail">
                                    <img src="${e.target.result}" alt="${file.name}">
                                </div>
                                <div class="image-info">
                                    <p>${file.name}</p>
                                    <p>${img.width} × ${img.height} px</p>
                                    <p>${formatFileSize(file.size)}</p>
                                </div>
                            `;
                            imageList.appendChild(imageItem);
                        };
                        img.src = e.target.result;
                    };
                    
                    reader.readAsDataURL(file);
                }
            } else {
                imageList.innerHTML = '<p>未选择图片</p>';
                uploadedImages.length = 0;
            }
        });
    }
    
    // 旋转按钮点击事件
    if (rotateLeft) {
        rotateLeft.addEventListener('click', () => {
            currentRotation = (currentRotation - 90) % 360;
            updateRotationDisplay();
        });
    }
    
    if (rotateRight) {
        rotateRight.addEventListener('click', () => {
            currentRotation = (currentRotation + 90) % 360;
            updateRotationDisplay();
        });
    }
    
    // 更新旋转显示
    function updateRotationDisplay() {
        const rotationDisplay = document.getElementById('rotation-display');
        if (rotationDisplay) {
            rotationDisplay.textContent = `${currentRotation}°`;
        }
    }
    
    // 预览按钮点击事件
    if (previewBtn && imagePreview) {
        previewBtn.addEventListener('click', () => {
            if (uploadedImages.length === 0) {
                alert('请先上传图片');
                return;
            }
            
            // 清空预览区域
            imagePreview.innerHTML = '';
            
            // 获取处理参数
            const width = parseInt(widthInput.value) || null;
            const height = parseInt(heightInput.value) || null;
            const watermark = watermarkText.value;
            const wmColor = watermarkColor.value;
            const wmOpacity = parseFloat(watermarkOpacity.value);
            
            // 预览处理后的图片
            uploadedImages.forEach(image => {
                const previewItem = document.createElement('div');
                previewItem.className = 'preview-item';
                
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');
                
                // 设置画布大小
                let newWidth = width || image.width;
                let newHeight = height || image.height;
                
                if (maintainRatio && maintainRatio.checked) {
                    const ratio = image.width / image.height;
                    if (width && !height) {
                        newHeight = Math.round(newWidth / ratio);
                    } else if (!width && height) {
                        newWidth = Math.round(newHeight * ratio);
                    }
                }
                
                canvas.width = newWidth;
                canvas.height = newHeight;
                
                // 应用旋转
                if (currentRotation !== 0) {
                    ctx.save();
                    ctx.translate(canvas.width / 2, canvas.height / 2);
                    ctx.rotate(currentRotation * Math.PI / 180);
                    ctx.drawImage(image.original, -newWidth / 2, -newHeight / 2, newWidth, newHeight);
                    ctx.restore();
                } else {
                    ctx.drawImage(image.original, 0, 0, newWidth, newHeight);
                }
                
                // 添加水印
                if (watermark) {
                    ctx.save();
                    ctx.globalAlpha = wmOpacity;
                    ctx.fillStyle = wmColor;
                    ctx.font = '20px Arial';
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'middle';
                    ctx.fillText(watermark, canvas.width / 2, canvas.height / 2);
                    ctx.restore();
                }
                
                // 添加预览图片
                previewItem.innerHTML = `
                    <div class="preview-image-container">
                        <img src="${canvas.toDataURL('image/jpeg', compressionQuality.value / 100)}" alt="${image.name}" class="preview-image">
                    </div>
                    <div class="preview-info">
                        <p>${image.name}</p>
                        <p>${newWidth} × ${newHeight} px</p>
                    </div>
                `;
                
                imagePreview.appendChild(previewItem);
            });
        });
    }
    
    // 处理按钮点击事件
    if (processBtn) {
        processBtn.addEventListener('click', () => {
            if (uploadedImages.length === 0) {
                alert('请先上传图片');
                return;
            }
            
            // 模拟处理过程
            processBtn.disabled = true;
            processBtn.textContent = '处理中...';
            
            setTimeout(() => {
                // 获取处理参数
                const width = parseInt(widthInput.value) || null;
                const height = parseInt(heightInput.value) || null;
                const watermark = watermarkText.value;
                const quality = compressionQuality.value;
                
                // 创建处理结果描述
                let processDescription = `已处理 ${uploadedImages.length} 张图片`;
                if (width || height) {
                    processDescription += `，调整大小为 ${width || '自动'} × ${height || '自动'}`;
                }
                if (currentRotation !== 0) {
                    processDescription += `，旋转 ${currentRotation}°`;
                }
                if (watermark) {
                    processDescription += `，添加水印`;
                }
                processDescription += `，压缩质量 ${quality}%`;
                
                alert(processDescription);
                
                // 恢复按钮状态
                processBtn.disabled = false;
                processBtn.textContent = '开始处理';
                
                // 在实际应用中，这里应该提供下载处理后的图片的功能
            }, 2000);
        });
    }
    
    // 初始化图片批量转换功能
    initImageConvertFunctions();
}

// 初始化图片批量转换功能
function initImageConvertFunctions() {
    const convertFiles = document.getElementById('convert-files');
    const convertFileList = document.getElementById('convert-file-list');
    const targetFormat = document.getElementById('target-format');
    const convertQuality = document.getElementById('convert-quality');
    const processBtn = document.querySelector('#image-convert .btn-process');
    
    // 文件上传处理
    if (convertFiles) {
        convertFiles.addEventListener('change', (e) => {
            const files = e.target.files;
            if (files.length > 0) {
                convertFileList.innerHTML = '';
                for (let i = 0; i < files.length; i++) {
                    const file = files[i];
                    const fileItem = document.createElement('div');
                    fileItem.className = 'file-item';
                    fileItem.innerHTML = `
                        <span class="file-name">${file.name}</span>
                        <span class="file-size">${formatFileSize(file.size)}</span>
                    `;
                    convertFileList.appendChild(fileItem);
                }
            } else {
                convertFileList.innerHTML = '<p>未选择图片</p>';
            }
        });
    }
    
    // 处理按钮点击事件
    if (processBtn) {
        processBtn.addEventListener('click', () => {
            const files = convertFiles.files;
            
            if (files.length === 0) {
                alert('请先选择图片');
                return;
            }
            
            // 获取转换参数
            const format = targetFormat.value;
            const quality = convertQuality.value;
            
            // 模拟处理过程
            processBtn.disabled = true;
            processBtn.textContent = '处理中...';
            
            setTimeout(() => {
                alert(`已完成转换！\n将 ${files.length} 张图片转换为 ${format.toUpperCase()} 格式，质量 ${quality}%`);
                processBtn.disabled = false;
                processBtn.textContent = '开始转换';
            }, 2000);
        });
    }
}

// 文件大小格式化
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}