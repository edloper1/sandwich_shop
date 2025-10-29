// JavaScript principal para Sandwich Shop

$(document).ready(function() {
    // Actualizar contador del carrito al cargar la página
    actualizarContadorCarrito();
    
    // Manejar formulario de agregar al carrito con AJAX
    $('.form-agregar-carrito').on('submit', function(e) {
        e.preventDefault();
        
        const form = $(this);
        const btn = form.find('button[type="submit"]');
        const btnText = btn.html();
        
        // Mostrar loading
        btn.html('<span class="loading-spinner"></span> Agregando...');
        btn.prop('disabled', true);
        
        $.ajax({
            url: form.attr('action'),
            type: 'POST',
            data: form.serialize(),
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            success: function(response) {
                if (response.success) {
                    // Actualizar contador del carrito
                    $('#cart-count').text(response.total_items);
                    
                    // Mostrar notificación de éxito
                    mostrarToast('Producto agregado al carrito', 'success');
                    
                    // Resetear cantidad
                    form.find('input[name="cantidad"]').val(1);
                }
            },
            error: function() {
                mostrarToast('Error al agregar el producto', 'error');
            },
            complete: function() {
                // Restaurar botón
                btn.html(btnText);
                btn.prop('disabled', false);
            }
        });
    });
    
    // Manejar cambios de cantidad en el carrito
    $('.cantidad-input').on('change', function() {
        const input = $(this);
        const itemId = input.data('item-id');
        const cantidad = input.val();
        
        if (cantidad < 1) {
            input.val(1);
            return;
        }
        
        // Actualizar cantidad vía AJAX
        actualizarCantidadItem(itemId, cantidad);
    });
    
    // Botones para incrementar/decrementar cantidad
    $('.btn-cantidad').on('click', function() {
        const btn = $(this);
        const input = btn.siblings('.cantidad-input');
        const accion = btn.data('accion');
        let cantidad = parseInt(input.val());
        
        if (accion === 'incrementar') {
            cantidad++;
        } else if (accion === 'decrementar' && cantidad > 1) {
            cantidad--;
        }
        
        input.val(cantidad);
        
        // Si está en el carrito, actualizar
        if (input.data('item-id')) {
            actualizarCantidadItem(input.data('item-id'), cantidad);
        }
    });
    
    // Manejar eliminación de items del carrito
    $('.btn-eliminar-item').on('click', function(e) {
        e.preventDefault();
        
        if (confirm('¿Estás seguro de que quieres eliminar este producto del carrito?')) {
            const url = $(this).attr('href');
            
            $.ajax({
                url: url,
                type: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                },
                success: function(response) {
                    if (response.success) {
                        location.reload(); // Recargar la página para mostrar cambios
                    }
                },
                error: function() {
                    mostrarToast('Error al eliminar el producto', 'error');
                }
            });
        }
    });
    
    // Filtros de tipo de entrega en checkout
    $('input[name="tipo_entrega"]').on('change', function() {
        const tipoEntrega = $(this).val();
        const direccionField = $('#id_direccion_entrega').closest('.form-group');
        
        if (tipoEntrega === 'delivery') {
            direccionField.show();
            $('#id_direccion_entrega').prop('required', true);
            actualizarTotalCheckout(5.00); // Agregar costo de delivery
        } else {
            direccionField.hide();
            $('#id_direccion_entrega').prop('required', false);
            actualizarTotalCheckout(0); // Sin costo de delivery
        }
    });
    
    // Búsqueda en tiempo real
    let searchTimeout;
    $('#search-input').on('input', function() {
        const query = $(this).val();
        
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(function() {
            if (query.length >= 2) {
                buscarProductos(query);
            }
        }, 300);
    });

    // Marcar pestaña activa en la navegación (mejora UX)
    const path = window.location.pathname;
    $('.navbar-nav .nav-link').each(function() {
        const href = $(this).attr('href');
        if (href && path.startsWith(href)) {
            $(this).addClass('active');
        }
    });
});

// Función para actualizar contador del carrito
function actualizarContadorCarrito() {
    $.ajax({
        url: '/carrito/info/',
        type: 'GET',
        success: function(response) {
            $('#cart-count').text(response.total_items);
        },
        error: function() {
            console.log('Error al obtener información del carrito');
        }
    });
}

// Función para actualizar cantidad de un item
function actualizarCantidadItem(itemId, cantidad) {
    $.ajax({
        url: `/carrito/actualizar/${itemId}/`,
        type: 'POST',
        data: {
            'cantidad': cantidad,
            'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
        },
        success: function() {
            // Recalcular totales en la página
            recalcularTotales();
            actualizarContadorCarrito();
        },
        error: function() {
            mostrarToast('Error al actualizar la cantidad', 'error');
        }
    });
}

// Función para recalcular totales del carrito
function recalcularTotales() {
    let subtotal = 0;
    
    $('.carrito-item').each(function() {
        const precio = parseFloat($(this).find('.precio-unitario').text());
        const cantidad = parseInt($(this).find('.cantidad-input').val());
        const total = precio * cantidad;
        
        $(this).find('.total-item').text(total.toFixed(2));
        subtotal += total;
    });
    
    $('#subtotal').text(subtotal.toFixed(2));
    
    // Calcular total con delivery si aplica
    const costoDelivery = parseFloat($('#costo-delivery').text()) || 0;
    const total = subtotal + costoDelivery;
    $('#total-final').text(total.toFixed(2));
}

// Función para actualizar total en checkout
function actualizarTotalCheckout(costoDelivery) {
    const subtotal = parseFloat($('#subtotal-checkout').text());
    const total = subtotal + costoDelivery;
    
    $('#costo-delivery-checkout').text(costoDelivery.toFixed(2));
    $('#total-checkout').text(total.toFixed(2));
}

// Función para mostrar notificaciones toast
function mostrarToast(mensaje, tipo) {
    const toastHtml = `
        <div class="toast align-items-center text-white bg-${tipo === 'success' ? 'success' : 'danger'} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    ${mensaje}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    // Crear container de toasts si no existe
    if (!$('#toast-container').length) {
        $('body').append('<div id="toast-container" class="position-fixed top-0 end-0 p-3" style="z-index: 11;"></div>');
    }
    
    const $toast = $(toastHtml);
    $('#toast-container').append($toast);
    
    const toast = new bootstrap.Toast($toast[0]);
    toast.show();
    
    // Eliminar el toast después de que se oculte
    $toast.on('hidden.bs.toast', function() {
        $(this).remove();
    });
}

// Función para búsqueda de productos
function buscarProductos(query) {
    $.ajax({
        url: '/catalogo/',
        type: 'GET',
        data: { 'q': query },
        success: function(response) {
            // Actualizar resultados de búsqueda
            // Esta función puede expandirse para búsqueda AJAX sin recargar página
            console.log('Búsqueda realizada:', query);
        }
    });
}

// Animaciones de scroll
$(window).on('scroll', function() {
    const scrolled = $(window).scrollTop();
    const parallax = $('.hero-section');
    const speed = scrolled * 0.5;
    
    parallax.css('transform', `translateY(${speed}px)`);
});

// Lazy loading para imágenes
$(document).ready(function() {
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });

    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
});