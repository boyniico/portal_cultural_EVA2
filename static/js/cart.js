let cart = JSON.parse(localStorage.getItem('portal_cart')) || [];

function saveCart() {
    localStorage.setItem('portal_cart', JSON.stringify(cart));
    updateCartUI();
}

function updateCartUI() {
    const cartItemsContainer = document.getElementById('cart-items');
    const cartCount = document.getElementById('cart-count');
    const cartTotal = document.getElementById('cart-total');
    const btnCheckout = document.getElementById('btn-checkout');

    if (!cartItemsContainer) return;

    cartItemsContainer.innerHTML = '';
    let total = 0;
    let totalCount = 0;

    if (cart.length === 0) {
        cartItemsContainer.innerHTML = `<p class="text-center text-muted my-5">Tu carrito está vacío por ahora.</p>`;
        cartTotal.textContent = '$0 CLP';
        cartCount.textContent = '0';
        if (btnCheckout) btnCheckout.disabled = true;
        return;
    }

    cart.forEach((item, index) => {
        const price = Number(item.price) || 0;
        const quantity = Number(item.quantity) || 1;
        
        // Calculamos el subtotal para este producto en específico
        const subtotal = price * quantity;

        total += subtotal;
        totalCount += quantity;

        const imageHtml = item.image 
            ? `<img src="${item.image}" alt="${item.title}" style="width: 45px; height: 45px; object-fit: cover;" class="rounded me-2">` 
            : `<div class="bg-secondary rounded me-2 d-flex align-items-center justify-content-center text-white" style="width: 45px; height: 45px; font-size: 10px;">Sin foto</div>`;

            cartItemsContainer.innerHTML += `
                <div class="d-flex justify-content-between align-items-center mb-3 border-bottom pb-2 custom-color-border-accent">
                    <div class="d-flex align-items-center">
                        ${imageHtml}
                        <div>
                            <h6 class="mb-0 fw-bold custom-color-text-dark" style="font-size: 0.85rem;">${item.title || 'Producto'}</h6>
                            <small class="custom-color-text-muted" style="font-size: 0.75rem;">$${price.toLocaleString('es-CL')} c/u</small>
                            
                            <!-- Controles de cantidad -->
                            <div class="input-group input-group-sm mt-1" style="width: 100px;">
                                <button class="btn btn-outline-secondary btn-sm px-1 py-0" onclick="changeQuantity(${index}, -1)">-</button>
                                <span class="form-control form-control-sm text-center custom-color-card custom-color-text-dark px-0" style="font-size: 0.8rem;">${quantity}</span>
                                <button class="btn btn-outline-secondary btn-sm px-1 py-0" onclick="changeQuantity(${index}, 1)">+</button>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Subtotal y eliminar -->
                    <div class="text-end ms-2">
                        <span class="d-block fw-bold custom-color-text-dark" style="font-size: 0.85rem;">$${subtotal.toLocaleString('es-CL')}</span>
                        <button class="btn btn-sm btn-outline-danger border-0 p-0 mt-1" onclick="removeItem(${index})" title="Eliminar">✕</button>
                    </div>
                </div>
            `;
    });

    cartTotal.textContent = `$${total.toLocaleString('es-CL')} CLP`;
    cartCount.textContent = totalCount;
    if (btnCheckout) btnCheckout.disabled = false;
}

function changeQuantity(index, delta) {
    const item = cart[index];
    const newQuantity = item.quantity + delta;

    if (newQuantity <= 0) {
        removeItem(index);
        return;
    }

    // Validar contra el stock disponible que trajimos en data-stock
    if (delta > 0 && newQuantity > item.stock) {
        Swal.fire({
            icon: 'warning',
            title: 'Stock límite',
            text: 'No hay más unidades disponibles en bodega.',
            timer: 1500,
            showConfirmButton: false
        });
        return;
    }

    item.quantity = newQuantity;
    saveCart();
}

function removeItem(index) {
    cart.splice(index, 1);
    saveCart();
}

// Función global conectada al botón mediante onclick="addToCart(this)"
window.addToCart = function(button) {
    const id = button.getAttribute('data-id');
    const title = button.getAttribute('data-title');
    const price = parseFloat(button.getAttribute('data-price')) || 0;
    const type = button.getAttribute('data-type');
    const stock = parseInt(button.getAttribute('data-stock')) || 0;
    const image = button.getAttribute('data-image') || ''; // Captura la imagen de media/

    const existingItem = cart.find(item => item.id === id && item.type === type);
    
    if (existingItem) {
        if (existingItem.quantity < stock) {
            existingItem.quantity += 1;
        } else {
            Swal.fire({
                icon: 'warning',
                title: 'Stock límite',
                text: 'No puedes agregar más unidades de las disponibles en bodega.',
                timer: 2000,
                showConfirmButton: false
            });
            return;
        }
    } else {
        cart.push({ id, title, price, type, quantity: 1, stock, image });
    }

    saveCart();

    const offcanvasEl = document.getElementById('cartOffcanvas');
    if (offcanvasEl) {
        const bsOffcanvas = new bootstrap.Offcanvas(offcanvasEl);
        bsOffcanvas.show();
    }
};

// Evento de Checkout con FETCH conectado al backend de Django
document.addEventListener('click', function(event) {
    if (event.target && event.target.id === 'btn-checkout') {
        if (cart.length === 0) return;

        const cartOffcanvasEl = document.getElementById('cartOffcanvas');
        const bsOffcanvas = bootstrap.Offcanvas.getInstance(cartOffcanvasEl);
        if (bsOffcanvas) bsOffcanvas.hide();

        Swal.fire({
            title: 'Procesando pago...',
            text: 'Actualizando stock en el servidor...',
            allowOutsideClick: false,
            didOpen: () => { Swal.showLoading(); }
        });

        fetch('/api/checkout/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ cart: cart })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                cart = [];
                saveCart();

                Swal.fire({
                    icon: 'success',
                    title: '¡Compra Exitosa! 🎉',
                    html: `
                        <p>Pedido procesado en la base de datos.</p>
                        <div class="text-start bg-light p-3 rounded mt-2">
                            <p class="mb-1"><strong>N° de Orden:</strong> #${data.order_num}</p>
                            <p class="mb-0"><strong>Total Pagado:</strong> $${data.total.toLocaleString('es-CL')} CLP</p>
                        </div>
                    `,
                    confirmButtonText: 'Entendido',
                    confirmButtonColor: '#3085d6'
                }).then(() => {
                    window.location.href = window.location.href;
                });
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Error en la compra',
                    text: data.error || 'No se pudo procesar el stock.'
                });
            }
        })
        .catch(error => {
            console.error('Error de red:', error);
            Swal.fire('Error', 'Ocurrió un problema de conexión con el servidor.', 'error');
        });
    }
});

document.addEventListener('DOMContentLoaded', () => {
    updateCartUI();
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}