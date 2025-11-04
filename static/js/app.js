/**
 * Todo Uygulaması JavaScript Dosyası
 */

document.addEventListener('DOMContentLoaded', function() {
    // CSRF Token'ı al
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    
    // Bildirim gösterme fonksiyonu
    function showNotification(message, type = 'success') {
        const notification = document.createElement('div');
        notification.className = `notification ${type === 'success' ? 'notification-success' : 'notification-error'}`;
        notification.textContent = message;
        document.body.appendChild(notification);
        
        // 3 saniye sonra bildirim kaybolsun
        setTimeout(() => {
            notification.classList.add('opacity-0');
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 3000);
    }
    
    
    // Sürükle-bırak işlevselliği
    if (typeof Sortable !== 'undefined') {
        // Pano sıralama
        const boardContainer = document.getElementById('board-container');
        if (boardContainer) {
            new Sortable(boardContainer, {
                animation: 150,
                ghostClass: 'sortable-ghost',
                chosenClass: 'sortable-chosen',
                dragClass: 'sortable-drag',
                onEnd: function(evt) {
                    const boardId = evt.item.getAttribute('data-board-id');
                    const newIndex = evt.newIndex;
                    
                    // AJAX isteği ile pano sırasını güncelle
                    fetch('/boards/reorder/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrfToken
                        },
                        body: JSON.stringify({
                            board_id: boardId,
                            new_order: newIndex
                        })
                    })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Sıralama güncellenirken bir hata oluştu');
                        }
                        return response.json();
                    })
                    .then(data => {
                        if (data.success) {
                            showNotification('Pano sırası güncellendi');
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        showNotification(error.message, 'error');
                    });
                }
            });
        }
        
        // Görev sıralama
        document.querySelectorAll('.task-list').forEach(el => {
            new Sortable(el, {
                group: 'tasks',
                animation: 150,
                ghostClass: 'sortable-ghost',
                chosenClass: 'sortable-chosen',
                dragClass: 'sortable-drag',
                onEnd: function(evt) {
                    const taskId = evt.item.getAttribute('data-task-id');
                    const newStatus = evt.to.getAttribute('data-status');
                    const boardId = evt.to.getAttribute('data-board-id');
                    const newIndex = evt.newIndex;
                    
                    // `newStatus` string değerini boolean değere dönüştür
                    let statusBoolean;
                    if (newStatus === 'todo') {
                        statusBoolean = true; // Yapılacak
                    } else if (newStatus === 'done') {
                        statusBoolean = false; // Tamamlandı
                    } else {
                        // Varsayılan veya hata durumu, mevcut durumu koru
                        statusBoolean = evt.item.closest('.task-list').getAttribute('data-status') === 'todo' ? true : false; // Mevcut listeye göre belirle
                    }

                    // AJAX isteği ile görev durumunu ve sırasını güncelle
                    fetch('/tasks/reorder/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrfToken
                        },
                        body: JSON.stringify({
                            task_id: taskId,
                            board_id: boardId,
                            new_status: statusBoolean, // Boolean değeri gönder
                            new_order: newIndex
                        })
                    })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Görev güncellenirken bir hata oluştu');
                        }
                        return response.json();
                    })
                    .then(data => {
                        if (data.success) {
                            showNotification(data.message || 'Görev güncellendi');
                            // Sayfayı yenile (görevlerin doğru listeye taşınması için)
                            window.location.reload();
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        showNotification(error.message, 'error');
                    });
                }
            });
        });
    }
    
    
    // Mobil menü açma/kapama
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }
    
    // Otomatik kaybolacak mesajlar
    const messages = document.querySelectorAll('.message');
    messages.forEach(message => {
        setTimeout(() => {
            message.classList.add('opacity-0');
            setTimeout(() => {
                message.remove();
            }, 300);
        }, 5000);
    });
}); 