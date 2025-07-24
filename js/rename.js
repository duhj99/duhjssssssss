// 文件重命名功能
function initRenameFunctions() {
    // 批量重命名功能
    initBatchRename();
    
    // 序列化重命名功能
    initSequenceRename();
    
    // 从Excel导入规则功能
    initExcelRename();
}

// 初始化批量重命名功能
function initBatchRename() {
    const renameFiles = document.getElementById('rename-files');
    const fileList = document.getElementById('rename-file-list');
    const renameOperation = document.getElementById('rename-operation');
    const prefixOption = document.getElementById('add-prefix-option');
    const suffixOption = document.getElementById('add-suffix-option');
    const replaceOption = document.getElementById('replace-option');
    const removeOption = document.getElementById('remove-option');
    const regexOption = document.getElementById('regex-option');
    const previewBtn = document.querySelector('#batch-rename .btn-preview');
    const processBtn = document.querySelector('#batch-rename .btn-process');
    const previewContent = document.querySelector('#batch-rename .preview-content');
    
    // 重命名操作选择
    if (renameOperation) {
        renameOperation.addEventListener('change', () => {
            // 隐藏所有选项
            prefixOption.style.display = 'none';
            suffixOption.style.display = 'none';
            replaceOption.style.display = 'none';
            removeOption.style.display = 'none';
            regexOption.style.display = 'none';
            
            // 显示选中的选项
            switch(renameOperation.value) {
                case 'add-prefix':
                    prefixOption.style.display = 'block';
                    break;
                case 'add-suffix':
                    suffixOption.style.display = 'block';
                    break;
                case 'replace':
                    replaceOption.style.display = 'block';
                    break;
                case 'remove':
                    removeOption.style.display = 'block';
                    break;
                case 'regex':
                    regexOption.style.display = 'block';
                    break;
            }
        });
    }
    
    // 文件上传处理
    if (renameFiles) {
        renameFiles.addEventListener('change', (e) => {
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
            const files = renameFiles.files;
            
            if (files.length === 0) {
                alert('请先选择文件');
                return;
            }
            
            // 获取重命名操作和参数
            const operation = renameOperation.value;
            let param1 = '', param2 = '';
            let beforeExtension = false;
            
            switch(operation) {
                case 'add-prefix':
                    param1 = document.getElementById('prefix-text').value;
                    break;
                case 'add-suffix':
                    param1 = document.getElementById('suffix-text').value;
                    beforeExtension = document.getElementById('before-extension').checked;
                    break;
                case 'replace':
                    param1 = document.getElementById('replace-from').value;
                    param2 = document.getElementById('replace-to').value;
                    break;
                case 'remove':
                    param1 = document.getElementById('remove-text').value;
                    break;
                case 'regex':
                    param1 = document.getElementById('regex-pattern').value;
                    param2 = document.getElementById('regex-replacement').value;
                    break;
            }
            
            // 清空预览区域
            previewContent.innerHTML = '';
            
            // 预览重命名结果
            const previewTable = document.createElement('table');
            previewTable.className = 'preview-table';
            previewTable.innerHTML = `
                <thead>
                    <tr>
                        <th>原文件名</th>
                        <th>新文件名</th>
                    </tr>
                </thead>
                <tbody></tbody>
            `;
            
            const tbody = previewTable.querySelector('tbody');
            
            for (let i = 0; i < files.length; i++) {
                const file = files[i];
                const fileName = file.name;
                const fileExt = fileName.lastIndexOf('.') !== -1 ? fileName.substring(fileName.lastIndexOf('.')) : '';
                const fileNameWithoutExt = fileName.lastIndexOf('.') !== -1 ? fileName.substring(0, fileName.lastIndexOf('.')) : fileName;
                
                let newName = '';
                
                switch(operation) {
                    case 'add-prefix':
                        newName = param1 + fileName;
                        break;
                    case 'add-suffix':
                        if (beforeExtension && fileExt) {
                            newName = fileNameWithoutExt + param1 + fileExt;
                        } else {
                            newName = fileName + param1;
                        }
                        break;
                    case 'replace':
                        newName = fileName.replace(new RegExp(param1, 'g'), param2);
                        break;
                    case 'remove':
                        newName = fileName.replace(new RegExp(param1, 'g'), '');
                        break;
                    case 'regex':
                        try {
                            const regex = new RegExp(param1, 'g');
                            newName = fileName.replace(regex, param2);
                        } catch (e) {
                            newName = '正则表达式错误';
                        }
                        break;
                }
                
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${fileName}</td>
                    <td>${newName}</td>
                `;
                tbody.appendChild(row);
            }
            
            previewContent.appendChild(previewTable);
        });
    }
    
    // 处理按钮点击事件
    if (processBtn) {
        processBtn.addEventListener('click', () => {
            const files = renameFiles.files;
            
            if (files.length === 0) {
                alert('请先选择文件');
                return;
            }
            
            // 获取重命名操作
            const operation = renameOperation.value;
            
            // 模拟处理过程
            processBtn.disabled = true;
            processBtn.textContent = '处理中...';
            
            setTimeout(() => {
                alert(`已完成重命名！\n处理了 ${files.length} 个文件`);
                processBtn.disabled = false;
                processBtn.textContent = '开始重命名';
            }, 2000);
        });
    }
}

// 初始化序列化重命名功能
function initSequenceRename() {
    const sequenceFiles = document.getElementById('sequence-files');
    const fileList = document.getElementById('sequence-file-list');
    const sequenceType = document.getElementById('sequence-type');
    const numberOption = document.getElementById('number-option');
    const dateOption = document.getElementById('date-option');
    const customOption = document.getElementById('custom-option');
    const previewBtn = document.querySelector('#sequence-rename .btn-preview');
    const processBtn = document.querySelector('#sequence-rename .btn-process');
    const previewContent = document.querySelector('#sequence-rename .preview-content');
    
    // 序列化方式选择
    if (sequenceType) {
        sequenceType.addEventListener('change', () => {
            // 隐藏所有选项
            numberOption.style.display = 'none';
            dateOption.style.display = 'none';
            customOption.style.display = 'none';
            
            // 显示选中的选项
            switch(sequenceType.value) {
                case 'number':
                    numberOption.style.display = 'block';
                    break;
                case 'date':
                    dateOption.style.display = 'block';
                    break;
                case 'custom':
                    customOption.style.display = 'block';
                    break;
            }
        });
    }
    
    // 文件上传处理
    if (sequenceFiles) {
        sequenceFiles.addEventListener('change', (e) => {
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
            const files = sequenceFiles.files;
            
            if (files.length === 0) {
                alert('请先选择文件');
                return;
            }
            
            // 获取序列化参数
            const type = sequenceType.value;
            const keepExtension = document.getElementById('keep-extension').checked;
            
            // 清空预览区域
            previewContent.innerHTML = '';
            
            // 预览重命名结果
            const previewTable = document.createElement('table');
            previewTable.className = 'preview-table';
            previewTable.innerHTML = `
                <thead>
                    <tr>
                        <th>原文件名</th>
                        <th>新文件名</th>
                    </tr>
                </thead>
                <tbody></tbody>
            `;
            
            const tbody = previewTable.querySelector('tbody');
            
            for (let i = 0; i < files.length; i++) {
                const file = files[i];
                const fileName = file.name;
                const fileExt = fileName.lastIndexOf('.') !== -1 ? fileName.substring(fileName.lastIndexOf('.')) : '';
                const fileNameWithoutExt = fileName.lastIndexOf('.') !== -1 ? fileName.substring(0, fileName.lastIndexOf('.')) : fileName;
                
                let newName = '';
                
                switch(type) {
                    case 'number':
                        const format = document.getElementById('number-format').value;
                        const startNumber = parseInt(document.getElementById('start-number').value) || 1;
                        const step = parseInt(document.getElementById('number-step').value) || 1;
                        const digits = parseInt(document.getElementById('number-digits').value) || 2;
                        
                        const num = startNumber + (i * step);
                        const paddedNum = num.toString().padStart(digits, '0');
                        newName = format.replace('{n}', paddedNum);
                        break;
                    case 'date':
                        const dateFormat = document.getElementById('date-format').value;
                        const datePattern = document.getElementById('date-pattern').value;
                        
                        const now = new Date();
                        let dateStr = '';
                        
                        switch(datePattern) {
                            case 'yyyy-MM-dd':
                                dateStr = `${now.getFullYear()}-${(now.getMonth() + 1).toString().padStart(2, '0')}-${now.getDate().toString().padStart(2, '0')}`;
                                break;
                            case 'yyyyMMdd':
                                dateStr = `${now.getFullYear()}${(now.getMonth() + 1).toString().padStart(2, '0')}${now.getDate().toString().padStart(2, '0')}`;
                                break;
                            case 'yyyy-MM-dd_HH-mm':
                                dateStr = `${now.getFullYear()}-${(now.getMonth() + 1).toString().padStart(2, '0')}-${now.getDate().toString().padStart(2, '0')}_${now.getHours().toString().padStart(2, '0')}-${now.getMinutes().toString().padStart(2, '0')}`;
                                break;
                            case 'yyyyMMdd_HHmm':
                                dateStr = `${now.getFullYear()}${(now.getMonth() + 1).toString().padStart(2, '0')}${now.getDate().toString().padStart(2, '0')}_${now.getHours().toString().padStart(2, '0')}${now.getMinutes().toString().padStart(2, '0')}`;
                                break;
                        }
                        
                        newName = dateFormat.replace('{date}', dateStr);
                        break;
                    case 'custom':
                        const customFormat = document.getElementById('custom-format').value;
                        const startNum = parseInt(document.getElementById('start-number').value) || 1;
                        const numStep = parseInt(document.getElementById('number-step').value) || 1;
                        
                        const customNum = startNum + (i * numStep);
                        newName = customFormat
                            .replace('{name}', fileNameWithoutExt)
                            .replace('{n}', customNum)
                            .replace('{ext}', fileExt);
                        break;
                }
                
                if (keepExtension && fileExt) {
                    if (!newName.endsWith(fileExt)) {
                        newName += fileExt;
                    }
                }
                
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${fileName}</td>
                    <td>${newName}</td>
                `;
                tbody.appendChild(row);
            }
            
            previewContent.appendChild(previewTable);
        });
    }
    
    // 处理按钮点击事件
    if (processBtn) {
        processBtn.addEventListener('click', () => {
            const files = sequenceFiles.files;
            
            if (files.length === 0) {
                alert('请先选择文件');
                return;
            }
            
            // 获取序列化方式
            const type = sequenceType.value;
            
            // 模