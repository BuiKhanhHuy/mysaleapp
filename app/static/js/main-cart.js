function addToCart(id, name, description, image, price) {
    fetch("/api/cart", {
        'method': 'post',
        'body': JSON.stringify({
            'id': id,
            'name': name,
            'description': description,
            'image': image,
            'price': price
        }),
        'headers': {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        console.log(data)
        var stats = document.getElementById('quantity-cart')
        stats.innerText = data["total_quantity"]
    })
}

function pay() {
    if (confirm('Bạn chắc chắn muốn thanh toán không?') == true) {
        fetch('/api/pay', {
            method: 'post'
        }).then(res => res.json()).then(data => {
            if(data.code == 200)
                location.reload()
        }).then(error => error(error))
    }
}

