// Word处理功能
function initWordFunctions() {
    const wordFiles = document.getElementById('word-files');
    const fileList = document.getElementById('word-file-list');
    const searchText = document.getElementById('search-text');
    const replaceText = document.getElementById('replace-text');
    const useRegex = document.getElementById('use-regex');
    const previewBtn = document.querySelector('#word-replace .btn-preview');
    const processBtn = document.querySelector('#word-replace .btn-process');
    const previewContent = document.querySelector('#word-replace .preview-content');
    
    // 文件上传处理
    if (wordFiles) {
        wordFiles.addEventListener('change', (e) => {
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
            const files = wordFiles.files;
            const search = searchText.value;
            const replace = replaceText.value;
            
            if (files.length === 0 || !search) {
                alert('请选择文件并输入查找内容');
                return;
            }
            
            // 这里只是模拟预览，实际应用中需要解析Word文档
            previewContent.innerHTML = `
                <div class="preview-item">
                    <h4>预览替换效果</h4>
                    <p>查找内容: <mark>${search}</mark></p>
                    <p>替换为: <span class="replaced-text">${replace}</span></p>
                    <p>将在 ${files.length} 个文件中执行替换</p>
                    <p class="note">注意: 这是模拟预览，实际替换需要后端支持</p>
                </div>
            `;
        });
    }
    
    // 处理按钮点击事件
    if (processBtn) {
        processBtn.addEventListener('click', () => {
            const files = wordFiles.files;
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
    
    // 初始化Word合并功能
    initWordMergeFunctions();
}

// 初始化Word合并功能
function initWordMergeFunctions() {
    const mergeFiles = document.getElementById('word-merge-files');
    const mergeFileList = document.getElementById('word-merge-file-list');
    const outputFilename = document.getElementById('word-output-filename');
    const processBtn = document.querySelector('#word-merge .btn-process');
    
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
                alert('请至少选择两个Word文件进行合并');
                return;
            }
            
            // 模拟处理过程
            processBtn.disabled = true;
            processBtn.textContent = '处理中...';
            
            setTimeout(() => {
                alert(`已完成合并！\n合并了 ${files.length} 个Word文件\n输出文件: ${outputFilename.value || '合并文档.docx'}`);
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