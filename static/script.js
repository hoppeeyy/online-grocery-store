function addToCart(productId) {
    const quantity = document.querySelector(`.product-card button[onclick="addToCart(${productId})"]`)
                   .previousElementSibling.value;
    
    fetch('/add_to_cart', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_id: productId, quantity: quantity })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            alert("Added to cart!");
        } else {
            alert("Error: " + data.message);
        }
    });
}