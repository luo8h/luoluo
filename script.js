document.addEventListener('DOMContentLoaded', function() {
    const addNameBtn = document.getElementById('addNameBtn');
    const addCourseBtn = document.getElementById('addCourseBtn');
    const table = document.querySelector('table');

    // 加载保存的数据
    loadTableData();

    // 添加姓名按钮点击事件
    addNameBtn.addEventListener('click', function() {
        const dialog = document.createElement('div');
        dialog.className = 'dialog';
        dialog.innerHTML = `
            <div class="dialog-content">
                <h3>添加姓名</h3>
                <input type="text" id="nameInput" placeholder="请输入姓名">
                <div class="dialog-buttons">
                    <button class="btn" onclick="this.closest('.dialog').remove()">取消</button>
                    <button class="btn" onclick="addName(this)">确定</button>
                </div>
            </div>
        `;
        document.body.appendChild(dialog);
    });

    // 添加课名按钮点击事件
    addCourseBtn.addEventListener('click', function() {
        const dialog = document.createElement('div');
        dialog.className = 'dialog';
        dialog.innerHTML = `
            <div class="dialog-content">
                <h3>添加课名</h3>
                <input type="text" id="courseInput" placeholder="请输入课名">
                <div class="dialog-buttons">
                    <button class="btn" onclick="this.closest('.dialog').remove()">取消</button>
                    <button class="btn" onclick="addCourse(this)">确定</button>
                </div>
            </div>
        `;
        document.body.appendChild(dialog);
    });

    // 双击单元格事件处理
    table.addEventListener('dblclick', function(e) {
        const cell = e.target.closest('td, th');
        if (!cell) return;

        cell.focus(); // 设置焦点，以便后续操作能找到正确的单元格

        const row = cell.parentElement;
        const rowIndex = row.rowIndex;
        const cellIndex = cell.cellIndex;

        // 如果是第一行（表头）且不是前两列
        if (rowIndex === 0 && cellIndex > 1) {
            showColumnOptions(cell);
        }
        // 如果是第一列或第二列（不包括表头）
        else if (rowIndex > 0 && (cellIndex === 0 || cellIndex === 1)) {
            showRowOptions(cell);
        }
        // 其他单元格（不包括前两列和第一行）
        else if (rowIndex > 0 && cellIndex > 1) {
            cell.textContent = '✓';
            saveTableData(); // 保存数据
        }
    });

    // 防止双击缩放
    document.addEventListener('dblclick', function(e) {
        if (e.target.tagName === 'TD') {
            e.preventDefault();
        }
    });
});

// 保存表格数据
function saveTableData() {
    const table = document.querySelector('table');
    const data = {
        headers: [],
        rows: []
    };

    // 保存表头
    const headerRow = table.querySelector('thead tr');
    headerRow.querySelectorAll('th').forEach(th => {
        data.headers.push(th.textContent);
    });

    // 保存数据行
    table.querySelectorAll('tbody tr').forEach(tr => {
        const rowData = [];
        tr.querySelectorAll('td').forEach((td, index) => {
            // 跳过序号列
            if (index === 0) {
                rowData.push(''); // 序号列保存为空，加载时会重新生成
            } else {
                rowData.push(td.textContent);
            }
        });
        data.rows.push(rowData);
    });

    localStorage.setItem('tableData', JSON.stringify(data));
}

// 加载表格数据
function loadTableData() {
    const savedData = localStorage.getItem('tableData');
    if (!savedData) return;

    const data = JSON.parse(savedData);
    const table = document.querySelector('table');
    
    // 恢复表头
    const headerRow = table.querySelector('thead tr');
    headerRow.innerHTML = ''; // 清空现有表头
    
    // 添加序号和姓名列
    const numberHeader = document.createElement('th');
    numberHeader.textContent = '序号';
    headerRow.appendChild(numberHeader);
    
    const nameHeader = document.createElement('th');
    nameHeader.textContent = '姓名';
    headerRow.appendChild(nameHeader);
    
    // 添加保存的课名列
    data.headers.forEach((header, index) => {
        if (index >= 2) { // 跳过序号和姓名列
            const th = document.createElement('th');
            th.textContent = header;
            headerRow.appendChild(th);
        }
    });
    
    // 清空现有表格内容
    const tbody = table.querySelector('tbody');
    tbody.innerHTML = '';

    // 恢复数据行
    data.rows.forEach((rowData, index) => {
        const tr = document.createElement('tr');
        rowData.forEach((cellData, cellIndex) => {
            const td = document.createElement('td');
            // 如果是序号列，使用当前行的索引+1
            if (cellIndex === 0) {
                td.textContent = index + 1;
            } else {
                td.textContent = cellData;
            }
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });
}

// 显示列操作选项
function showColumnOptions(cell) {
    const dialog = document.createElement('div');
    dialog.className = 'dialog';
    dialog.innerHTML = `
        <div class="dialog-content">
            <h3>选择操作</h3>
            <div class="dialog-buttons">
                <button class="btn primary-btn">删除</button>
                <button class="btn primary-btn">增加</button>
                <button class="btn secondary-btn">取消</button>
            </div>
        </div>
    `;
    
    // 添加事件监听器
    const deleteBtn = dialog.querySelector('.primary-btn');
    const addBtn = dialog.querySelector('.primary-btn:nth-child(2)');
    const cancelBtn = dialog.querySelector('.secondary-btn');
    
    deleteBtn.addEventListener('click', () => {
        deleteColumn(cell);
        dialog.remove();
    });
    
    addBtn.addEventListener('click', () => {
        dialog.remove();
        addColumn(cell);
    });
    
    cancelBtn.addEventListener('click', () => {
        dialog.remove();
    });
    
    document.body.appendChild(dialog);
}

// 显示行操作选项
function showRowOptions(cell) {
    const dialog = document.createElement('div');
    dialog.className = 'dialog';
    dialog.innerHTML = `
        <div class="dialog-content">
            <h3>选择操作</h3>
            <div class="dialog-buttons">
                <button class="btn primary-btn">删除</button>
                <button class="btn primary-btn">增加</button>
                <button class="btn secondary-btn">取消</button>
            </div>
        </div>
    `;
    
    // 添加事件监听器
    const deleteBtn = dialog.querySelector('.primary-btn');
    const addBtn = dialog.querySelector('.primary-btn:nth-child(2)');
    const cancelBtn = dialog.querySelector('.secondary-btn');
    
    deleteBtn.addEventListener('click', () => {
        deleteRow(cell);
        dialog.remove();
    });
    
    addBtn.addEventListener('click', () => {
        dialog.remove();
        addRow(cell);
    });
    
    cancelBtn.addEventListener('click', () => {
        dialog.remove();
    });
    
    document.body.appendChild(dialog);
}

// 删除列
function deleteColumn(cell) {
    if (!cell) return;
    
    const cellIndex = cell.cellIndex;
    const rows = document.querySelectorAll('tr');
    rows.forEach(row => {
        row.deleteCell(cellIndex);
    });

    // 保存数据
    saveTableData();
}

// 添加列
function addColumn(cell) {
    const dialog = document.createElement('div');
    dialog.className = 'dialog';
    dialog.innerHTML = `
        <div class="dialog-content">
            <h3>添加课名</h3>
            <input type="text" id="newCourseInput" placeholder="请输入课名" autofocus>
            <div class="dialog-buttons">
                <button class="btn secondary-btn">取消</button>
                <button class="btn primary-btn">确定</button>
            </div>
        </div>
    `;
    
    // 添加事件监听器
    const confirmBtn = dialog.querySelector('.primary-btn');
    const cancelBtn = dialog.querySelector('.secondary-btn');
    
    confirmBtn.addEventListener('click', () => {
        confirmAddColumn(cell);
        dialog.remove();
    });
    
    cancelBtn.addEventListener('click', () => {
        dialog.remove();
    });
    
    document.body.appendChild(dialog);
    
    // 自动聚焦输入框
    setTimeout(() => {
        const input = document.getElementById('newCourseInput');
        if (input) input.focus();
    }, 100);
}

// 确认添加列
function confirmAddColumn(cell) {
    const input = document.getElementById('newCourseInput');
    const courseName = input.value.trim();
    if (!courseName) return;

    if (!cell) return;

    const cellIndex = cell.cellIndex;
    const rows = document.querySelectorAll('tr');
    
    rows.forEach((row, index) => {
        const newCell = row.insertCell(cellIndex + 1);
        if (index === 0) {
            newCell.textContent = courseName;
        }
    });

    // 保存数据
    saveTableData();
}

// 删除行
function deleteRow(cell) {
    if (!cell) return;
    
    const row = cell.parentElement;
    row.remove();
    
    // 重新编号
    updateRowNumbers();
    
    // 保存数据
    saveTableData();
}

// 添加行
function addRow(cell) {
    const dialog = document.createElement('div');
    dialog.className = 'dialog';
    dialog.innerHTML = `
        <div class="dialog-content">
            <h3>添加姓名</h3>
            <input type="text" id="newNameInput" placeholder="请输入姓名" autofocus>
            <div class="dialog-buttons">
                <button class="btn secondary-btn">取消</button>
                <button class="btn primary-btn">确定</button>
            </div>
        </div>
    `;
    
    // 添加事件监听器
    const confirmBtn = dialog.querySelector('.primary-btn');
    const cancelBtn = dialog.querySelector('.secondary-btn');
    
    confirmBtn.addEventListener('click', () => {
        confirmAddRow(cell);
        dialog.remove();
    });
    
    cancelBtn.addEventListener('click', () => {
        dialog.remove();
    });
    
    document.body.appendChild(dialog);
    
    // 自动聚焦输入框
    setTimeout(() => {
        const input = document.getElementById('newNameInput');
        if (input) input.focus();
    }, 100);
}

// 确认添加行
function confirmAddRow(cell) {
    const input = document.getElementById('newNameInput');
    const name = input.value.trim();
    if (!name) return;

    if (!cell) return;

    const row = cell.parentElement;
    const newRow = document.createElement('tr');
    
    // 添加序号
    const numberCell = document.createElement('td');
    // 使用当前表格中的行数作为新行的序号
    const currentRowCount = document.querySelectorAll('tbody tr').length;
    numberCell.textContent = currentRowCount + 1;
    newRow.appendChild(numberCell);
    
    // 添加姓名
    const nameCell = document.createElement('td');
    nameCell.textContent = name;
    newRow.appendChild(nameCell);
    
    // 添加其他单元格
    const columnCount = row.cells.length;
    for (let i = 2; i < columnCount; i++) {
        const newCell = document.createElement('td');
        newRow.appendChild(newCell);
    }
    
    // 在当前行后插入新行
    row.insertAdjacentElement('afterend', newRow);
    
    // 重新编号
    updateRowNumbers();
    
    // 保存数据
    saveTableData();
}

// 更新行号
function updateRowNumbers() {
    const rows = document.querySelectorAll('tr:not(:first-child)');
    rows.forEach((row, index) => {
        row.cells[0].textContent = index + 1;
    });
}

// 添加姓名
function addName(button) {
    const input = document.getElementById('nameInput');
    const name = input.value.trim();
    if (!name) return;

    const tbody = document.querySelector('tbody');
    const newRow = document.createElement('tr');
    
    // 添加序号
    const numberCell = document.createElement('td');
    numberCell.textContent = tbody.children.length + 1;
    newRow.appendChild(numberCell);
    
    // 添加姓名
    const nameCell = document.createElement('td');
    nameCell.textContent = name;
    newRow.appendChild(nameCell);
    
    // 添加其他单元格
    const headerRow = document.querySelector('thead tr');
    const columnCount = headerRow.cells.length;
    for (let i = 2; i < columnCount; i++) {
        const newCell = document.createElement('td');
        newRow.appendChild(newCell);
    }
    
    tbody.appendChild(newRow);
    
    // 清空输入框并保持焦点
    input.value = '';
    input.focus();
    
    // 更改按钮文字为"继续"
    button.textContent = '继续';

    // 保存数据
    saveTableData();
}

// 添加课名
function addCourse(button) {
    const input = document.getElementById('courseInput');
    const courseName = input.value.trim();
    if (!courseName) return;

    const headerRow = document.querySelector('thead tr');
    const newHeaderCell = document.createElement('th');
    newHeaderCell.textContent = courseName;
    headerRow.appendChild(newHeaderCell);

    const rows = document.querySelectorAll('tbody tr');
    rows.forEach(row => {
        const newCell = document.createElement('td');
        row.appendChild(newCell);
    });

    // 清空输入框并保持焦点
    input.value = '';
    input.focus();
    
    // 更改按钮文字为"继续"
    button.textContent = '继续';

    // 保存数据
    saveTableData();
}