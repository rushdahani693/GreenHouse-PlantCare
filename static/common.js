// Common JavaScript functions for Greenhouse Manager application

// Generic search function that works with any table
function searchTable(inputId, tableId, countId) {
    const input = document.getElementById(inputId);
    const filter = input.value.toUpperCase();
    const table = document.getElementById(tableId);
    const tr = table.getElementsByTagName('tr');
    let visibleCount = 0;
    
    for (let i = 1; i < tr.length; i++) {
        // Get all cells in the row
        const tds = tr[i].getElementsByTagName('td');
        let found = false;
        
        // Check each cell for matching content
        for (let j = 0; j < tds.length; j++) {
            const cellValue = tds[j].textContent || tds[j].innerText;
            if (cellValue.toUpperCase().indexOf(filter) > -1) {
                found = true;
                break;
            }
        }
        
        if (found) {
            tr[i].style.display = '';
            visibleCount++;
        } else {
            tr[i].style.display = 'none';
        }
    }
    
    // Update the count if countId is provided
    if (countId) {
        const countElement = document.getElementById(countId);
        if (countElement) {
            countElement.textContent = visibleCount;
        }
    }
}

// Generic sort function that works with any table
function sortTable(tableId, columnIndex) {
    const table = document.getElementById(tableId);
    const tbody = table.tBodies[0];
    const rows = Array.from(tbody.querySelectorAll('tr'));
    
    const sortedRows = rows.sort((a, b) => {
        const aValue = a.cells[columnIndex].textContent.trim();
        const bValue = b.cells[columnIndex].textContent.trim();
        
        // Check if values are numbers
        const aNum = parseFloat(aValue.replace('$', '').replace(/[^0-9.-]+/g, ''));
        const bNum = parseFloat(bValue.replace('$', '').replace(/[^0-9.-]+/g, ''));
        
        if (!isNaN(aNum) && !isNaN(bNum)) {
            return aNum - bNum;
        }
        
        return aValue.localeCompare(bValue);
    });
    
    // Toggle sort direction on second click
    if (table.dataset.lastSort === String(columnIndex)) {
        sortedRows.reverse();
        table.dataset.lastSort = '';
    } else {
        table.dataset.lastSort = columnIndex;
    }
    
    tbody.innerHTML = '';
    sortedRows.forEach(row => tbody.appendChild(row));
}