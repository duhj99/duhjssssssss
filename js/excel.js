// Excel处理功能
function initExcelFunctions() {
    const excelFiles = document.getElementById('excel-files');
    const fileList = document.getElementById('excel-file-list');
    const searchText = document.getElementById('excel-search-text');
    const replaceText = document.getElementById('excel-replace-text');
    const useRegex = document.getElementById('excel-use-regex');
    const sheetRange = document.getElementById('sheet-range');
    const sheetNames = document.getElementById('sheet-names');
    const previewBtn = document.querySelector('#excel-replace .btn-preview');
    const processBtn = document.querySelector('#excel-replace .btn-process');
    const previewContent = document.querySelector('#excel-replace .preview-content');
    
    // 工作表范围选择
    if (sheetRange && sheetNames) {
        sheetRange.addEventListener('change', () => {
            if (sheetRange.value === 'selected') {
                sheetNames.style.display = 'block';
            } else {
                sheetNames.style.display = 'none';
            }
        });
    }
    
    // 文件上传处理
    if (excelFiles) {
        excelFiles.addEventListener('change', (e) => {
            const files = e.target.files;
            if (files.length > 0) {
                fileList.innerHTML = '';
                for (let i = 0; i < files.length; i++) {
                    const file = files[i];
                    const fileItem = document.createElement('div');
                    fileItem.className = 'file-item';
                    fileItem.innerHTML = `
                        <span class="file-name">${file.name}</span>
                        <span class="file-size">${formatFileSize(file.size)}</span>
                    `;
                    fileList.appendChild(fileItem);
                }
            } else {
                fileList.innerHTML = '<p>未选择文件</p>';
            }
        });
    }
    
    // 预览按钮点击事件
    if (previewBtn) {
        previewBtn.addEventListener('click', () => {
            const files = excelFiles.files;
            const search = searchText.value;
            const replace = replaceText.value;
            
            if (files.length === 0 || !search) {
                alert('请选择文件并输入查找内容');
                return;
            }
            
            // 这里只是模拟预览，实际应用中需要解析Excel文档
            previewContent.innerHTML = `
                <div class="preview-item">
                    <h4>预览替换效果</h4>
                    <p>查找内容: <mark>${search}</mark></p>
                    <p>替换为: <span class="replaced-text">${replace}</span></p>
                    <p>工作表范围: ${sheetRange.options[sheetRange.selectedIndex].text}</p>
                    ${sheetRange.value === 'selected' ? `<p>指定工作表: ${sheetNames.value || '未指定'}</p>` : ''}
                    <p>将在 ${files.length} 个文件中执行替换</p>
                    <p class="note">注意: 这是模拟预览，实际替换需要后端支持</p>
                </div>
            `;
        });
    }
    
    // 处理按钮点击事件
    if (processBtn) {
        processBtn.addEventListener('click', () => {
            const files = excelFiles.files;
            const search = searchText.value;
            const replace = replaceText.value;
            
            if (files.length === 0 || !search) {
                alert('请选择文件并输入查找内容');
                return;
            }
            
            // 模拟处理过程
            processBtn.disabled = true;
            processBtn.textContent = '处理中...';
            
            setTimeout(() => {
                alert(`已完成替换！\n在 ${files.length} 个文件中将 "${search}" 替换为 "${replace}"`);
                processBtn.disabled = false;
                processBtn.textContent = '开始处理';
            }, 2000);
        });
    }
    
    // 初始化Excel合并功能
    initExcelMergeFunctions();
}

// 初始化Excel合并功能
function initExcelMergeFunctions() {
    const mergeFiles = document.getElementById('excel-merge-files');
    const mergeFileList = document.getElementById('excel-merge-file-list');
    const removeDuplicates = document.getElementById('remove-duplicates');
    const outputFilename = document.getElementById('output-filename');
    const processBtn = document.querySelector('#excel-merge .btn-process');
    
    // 文件上传处理
    if (mergeFiles) {
        mergeFiles.addEventListener('change', (e) => {
            const files = e.target.files;
            if (files.length > 0) {
                mergeFileList.innerHTML = '';
                for (let i = 0; i < files.length; i++) {
                    const file = files[i];
                    const fileItem = document.createElement('div');
                    fileItem.className = 'file-item';
                    fileItem.innerHTML = `
                        <span class="file-name">${file.name}</span>
                        <span class="file-size">${formatFileSize(file.size)}</span>
                    `;
                    mergeFileList.appendChild(fileItem);
                }
            } else {
                mergeFileList.innerHTML = '<p>未选择文件</p>';
            }
        });
    }
    
    // 处理按钮点击事件
    if (processBtn) {
        processBtn.addEventListener('click', () => {
            const files = mergeFiles.files;
            
            if (files.length < 2) {
                alert('请至少选择两个Excel文件进行合并');
                return;
            }
            
            // 获取合并方式
            const mergeType = document.querySelector('input[name="merge-type"]:checked').value;
            
            // 模拟处理过程
            processBtn.disabled = true;
            processBtn.textContent = '处理中...';
            
            setTimeout(() => {
                let mergeTypeText = '';
                switch(mergeType) {
                    case 'row':
                        mergeTypeText = '按行合并';
                        break;
                    case 'column':
                        mergeTypeText = '按列合并';
                        break;
                    case 'sheet':
                        mergeTypeText = '按工作表合并';
                        break;
                }
                
                alert(`已完成合并！\n合并方式: ${mergeTypeText}\n合并文件数: ${files.length}\n输出文件: ${outputFilename.value}`);
                processBtn.disabled = false;
                processBtn.textContent = '开始合并';
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