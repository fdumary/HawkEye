/* Dashboard JavaScript */

// Load profile on page load
document.addEventListener('DOMContentLoaded', () => {
    loadProfile();
    checkAdminAccess();
});

function loadProfile() {
    fetch('/api/profile')
        .then(response => {
            if (response.status === 401) {
                window.location.href = '/login';
                return;
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                window.location.href = '/login';
                return;
            }

            // Update profile card
            document.getElementById('profileName').textContent = data.name;
            document.getElementById('profileRank').textContent = data.rank;
            document.getElementById('profileUnit').textContent = data.unit;
            document.getElementById('profileClearance').textContent = data.clearance_level;

            // Update user greeting
            document.getElementById('userGreeting').textContent = `Welcome, ${data.rank} ${data.name}`;

            // Display access areas
            displayAccessAreas(data.access_areas);

            // Update login time
            const now = new Date();
            document.getElementById('loginTime').textContent = now.toLocaleString();
        })
        .catch(error => {
            console.error('Error loading profile:', error);
            window.location.href = '/login';
        });
}

function displayAccessAreas(areas) {
    const container = document.getElementById('accessAreas');
    container.innerHTML = '';

    if (areas.length === 0) {
        container.innerHTML = '<p>No authorized areas</p>';
        return;
    }

    areas.forEach(area => {
        const item = document.createElement('div');
        item.className = 'access-item granted';
        item.textContent = formatAreaName(area);
        container.appendChild(item);
    });
}

function formatAreaName(area) {
    return area.replace(/_/g, ' ').toUpperCase();
}

function requestAreaAccess() {
    const area = document.getElementById('areaSelect').value;

    if (!area) {
        showAccessMessage('Please select an area', 'error');
        return;
    }

    fetch('/api/request-access', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ area: area })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAccessMessage('✓ ' + data.message, 'success');
        } else {
            showAccessMessage('✗ ' + data.message, 'error');
        }
    })
    .catch(error => {
        showAccessMessage('Error: ' + error.message, 'error');
    });
}

function showAccessMessage(text, type) {
    const messageEl = document.getElementById('accessMessage');
    messageEl.textContent = text;
    messageEl.className = 'message ' + type;
    messageEl.style.display = 'block';

    setTimeout(() => {
        messageEl.style.display = 'none';
    }, 5000);
}

function checkAdminAccess() {
    fetch('/api/profile')
        .then(response => response.json())
        .then(data => {
            if (data.clearance_level === 'TOP SECRET') {
                document.getElementById('adminPanel').style.display = 'block';
            }
        });
}

function viewAccessLog() {
    fetch('/api/access-log')
        .then(response => {
            if (response.status === 403) {
                showModal('Access Denied', '<p>You do not have permission to view this data.</p>');
                return;
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                showModal('Error', '<p>' + data.error + '</p>');
                return;
            }

            let html = '<table>';
            html += '<thead><tr><th>Soldier ID</th><th>Name</th><th>Timestamp</th><th>Status</th><th>Area</th></tr></thead>';
            html += '<tbody>';

            data.log.forEach(entry => {
                html += '<tr>';
                html += '<td>' + entry.soldier_id + '</td>';
                html += '<td>' + entry.name + '</td>';
                html += '<td>' + new Date(entry.timestamp).toLocaleString() + '</td>';
                html += '<td>' + entry.status + '</td>';
                html += '<td>' + entry.area + '</td>';
                html += '</tr>';
            });

            html += '</tbody></table>';
            showModal('Access Log', html);
        })
        .catch(error => {
            showModal('Error', '<p>' + error.message + '</p>');
        });
}

function viewAllPersonnel() {
    fetch('/api/all-personnel')
        .then(response => {
            if (response.status === 403) {
                showModal('Access Denied', '<p>You do not have permission to view this data.</p>');
                return;
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                showModal('Error', '<p>' + data.error + '</p>');
                return;
            }

            let html = '<table>';
            html += '<thead><tr><th>Soldier ID</th><th>Name</th><th>Rank</th><th>Unit</th><th>Clearance</th></tr></thead>';
            html += '<tbody>';

            Object.entries(data.personnel).forEach(([id, soldier]) => {
                html += '<tr>';
                html += '<td>' + id + '</td>';
                html += '<td>' + soldier.name + '</td>';
                html += '<td>' + soldier.rank + '</td>';
                html += '<td>' + soldier.unit + '</td>';
                html += '<td>' + soldier.clearance_level + '</td>';
                html += '</tr>';
            });

            html += '</tbody></table>';
            showModal('All Personnel', html);
        })
        .catch(error => {
            showModal('Error', '<p>' + error.message + '</p>');
        });
}

function showModal(title, content) {
    document.getElementById('modalTitle').textContent = title;
    document.getElementById('modalBody').innerHTML = content;
    document.getElementById('modal').style.display = 'flex';
}

function closeModal() {
    document.getElementById('modal').style.display = 'none';
}

function logout() {
    if (confirm('Are you sure you want to logout?')) {
        fetch('/api/logout', { method: 'POST' })
            .then(() => {
                window.location.href = '/';
            });
    }
}

// Close modal when clicking outside
window.addEventListener('click', (event) => {
    const modal = document.getElementById('modal');
    if (event.target === modal) {
        closeModal();
    }
});
