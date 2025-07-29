// Word处理功能
// 将函数导出到全局作用域，使main.js可以访问
window.initWordFunctions = function() {
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
            const regex = useRegex.checked;
            
            if (files.length === 0 || !search) {
                alert('请选择文件并输入查找内容');
                return;
            }
            
            // 显示处理状态
            processBtn.disabled = true;
            processBtn.textContent = '处理中...';
            
            // 创建FormData对象
            const formData = new FormData();
            
            // 添加多个文件
            for (let i = 0; i < files.length; i++) {
                formData.append('files', files[i]);
            }
            
            // 创建符合后端API期望的JSON请求
            const requestData = {
                replacements: [
                    {
                        find_text: search,
                        replace_text: replace
                    }
                ],
                use_regex: regex
            };
            
            // 将JSON对象转换为字符串并添加到FormData
            formData.append('request', JSON.stringify(requestData));
            
            // 发送API请求
            fetch('/api/word/batch-find-replace', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(data => {
                        throw new Error(data.detail || '处理失败');
                    });
                }
                return response.blob();
            })
            .then(blob => {
                // 创建下载链接
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'replaced_documents.zip';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                
                // 恢复按钮状态
                processBtn.disabled = false;
                processBtn.textContent = '开始处理';
                
                // 显示成功消息
                alert(`已完成替换！\n在 ${files.length} 个文件中将 "${search}" 替换为 "${replace}"`);
            })
            .catch(error => {
                console.error('Error:', error);
                alert(`处理失败: ${error.message}`);
                
                // 恢复按钮状态
                processBtn.disabled = false;
                processBtn.textContent = '开始处理';
            });
        });
    }
    
    // 初始化Word合并功能
    initWordMergeFunctions();
    
    // 初始化Word内容提取功能
    initWordExtractFunctions();
}

// 初始化Word内容提取功能
function initWordExtractFunctions() {
    const extractFiles = document.getElementById('word-extract-files');
    const extractFileList = document.getElementById('word-extract-file-list');
    const processBtn = document.querySelector('#word-extract .btn-process');
    
    // 文件上传处理
    if (extractFiles) {
        extractFiles.addEventListener('change', (e) => {
            const files = e.target.files;
            if (files.length > 0) {
                extractFileList.innerHTML = '';
                for (let i = 0; i < files.length; i++) {
                    const file = files[i];
                    const fileItem = document.createElement('div');
                    fileItem.className = 'file-item';
                    fileItem.innerHTML = `
                        <span class="file-name">${file.name}</span>
                        <span class="file-size">${formatFileSize(file.size)}</span>
                    `;
                    extractFileList.appendChild(fileItem);
                }
            } else {
                extractFileList.innerHTML = '<p>未选择文件</p>';
            }
        });
    }
    
    // 处理按钮点击事件
    if (processBtn) {
        processBtn.addEventListener('click', () => {
            const files = extractFiles.files;
            const extractType = document.querySelector('input[name="extract-type"]:checked').value;
            
            if (files.length === 0) {
                alert('请选择Word文件');
                return;
            }
            
            // 显示处理状态
            processBtn.disabled = true;
            processBtn.textContent = '处理中...';
            
            // 创建FormData对象
            const formData = new FormData();
            
            // 添加多个文件
            for (let i = 0; i < files.length; i++) {
                formData.append('files', files[i]);
            }
            
            formData.append('extract_type', extractType);
            
            // 发送API请求
            fetch('/api/word/extract', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(data => {
                        throw new Error(data.detail || '处理失败');
                    });
                }
                return response.json();
            })
            .then(data => {
                // 显示提取结果
                const resultArea = document.getElementById('extract-result');
                if (resultArea) {
                    resultArea.style.display = 'block';
                    
                    // 根据提取类型显示不同的结果
                    if (extractType === 'text') {
                        resultArea.querySelector('textarea').value = data.extracted_content.join('\n\n');
                    } else {
                        // 表格内容可能需要特殊处理
                        resultArea.querySelector('textarea').value = JSON.stringify(data.extracted_content, null, 2);
                    }
                    
                    // 添加复制内容功能
                    const copyBtn = resultArea.querySelector('.btn-copy');
                    if (copyBtn) {
                        copyBtn.addEventListener('click', () => {
                            const textarea = resultArea.querySelector('textarea');
                            textarea.select();
                            document.execCommand('copy');
                            alert('内容已复制到剪贴板');
                        });
                    }
                    
                    // 添加保存为文件功能
                    const saveBtn = resultArea.querySelector('.btn-save');
                    if (saveBtn) {
                        saveBtn.addEventListener('click', () => {
                            const content = resultArea.querySelector('textarea').value;
                            const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
                            const url = URL.createObjectURL(blob);
                            const a = document.createElement('a');
                            a.href = url;
                            a.download = `提取内容_${new Date().toISOString().slice(0, 10)}.txt`;
                            document.body.appendChild(a);
                            a.click();
                            document.body.removeChild(a);
                            URL.revokeObjectURL(url);
                        });
                    }
                }
                
                // 恢复按钮状态
                processBtn.disabled = false;
                processBtn.textContent = '开始提取';
                
                // 显示成功消息
                alert(`已完成提取！\n从 ${files.length} 个文件中提取了 ${extractType === 'text' ? '文本' : '表格'}`);
            })
            .catch(error => {
                console.error('Error:', error);
                alert(`处理失败: ${error.message}`);
                
                // 恢复按钮状态
                processBtn.disabled = false;
                processBtn.textContent = '开始提取';
            });
        });
    }
}

// 初始化Word合并功能
function initWordMergeFunctions() {
    const mergeFiles = document.getElementById('merge-files');
    const mergeFileList = document.getElementById('merge-file-list');
    const outputFilename = document.getElementById('output-filename');
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
            const filename = outputFilename.value || '合并文档';
            
            if (files.length < 2) {
                alert('请至少选择两个Word文件进行合并');
                return;
            }
            
            // 显示处理状态
            processBtn.disabled = true;
            processBtn.textContent = '处理中...';
            
            // 创建FormData对象
            const formData = new FormData();
            
            // 添加多个文件
            for (let i = 0; i < files.length; i++) {
                formData.append('files', files[i]);
            }
            
            // 注意：后端API不接收output_filename参数，所以我们不发送它
            // 但我们会在客户端保存时使用这个文件名
            
            // 发送API请求
            fetch('/api/word/merge', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(data => {
                        throw new Error(data.detail || '处理失败');
                    });
                }
                return response.blob();
            })
            .then(blob => {
                // 创建下载链接
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `${filename}.docx`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                
                // 恢复按钮状态
                processBtn.disabled = false;
                processBtn.textContent = '开始合并';
                
                // 显示成功消息
                alert(`已完成合并！\n合并了 ${files.length} 个Word文件\n输出文件: ${filename}.docx`);
            })
            .catch(error => {
                console.error('Error:', error);
                alert(`处理失败: ${error.message}`);
                
                // 恢复按钮状态
                processBtn.disabled = false;
                processBtn.textContent = '开始合并';
            });
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