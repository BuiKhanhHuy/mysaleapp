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
        fetch("/api/pay", {
            'method': 'post'
        }).then(res => res.json()).then(data => {
            if (data.code == 200)
                location.reload()
        }).then(error => error(error))
    }
}

function deleteItem(productId) {
    if (confirm('Bạn có chắc chắn xóa sản phẩm này ra khỏi giỏ hàng?') == true) {
        fetch('/api/delete-cart', {
            'method': 'delete',
            'body': JSON.stringify({
                'id': productId
            }),
            'headers': {
                'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then(data => {
            if (data.code === 200) {
                console.log(data.error)
                let item = document.getElementById(`item${productId}`)
                let totalQuan = document.getElementById("total-quan")
                let totalPri = document.getElementById("total-pri")

                item.style.display = 'none'
                totalQuan.innerText = `x ${data.total_quantity}`
                totalPri.innerText = (data.total_price).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',') + " VND"
                updateNumberCart(data.total_quantity)

                if (data.total_quantity === 0)
                    location.reload()
            } else if (data.code === 500) {
                alert(data.error)
            }
        }).catch(function (err) {
            console.log(err)
        })
    }
}

function updateNumberProductCart(object, productId, productPrice) {
    fetch('/api/update-cart', {
        'method': 'put',
        'body': JSON.stringify({
            'id': productId,
            'quantity': parseInt(object.value)
        }),
        'headers': {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        if (data.code === 200) {
            console.log(data.error)
            let itemQuan = document.getElementById(`item-quan${productId}`)
            let itemPri = document.getElementById(`item-pri${productId}`)
            let totalQuan = document.getElementById("total-quan")
            let totalPri = document.getElementById("total-pri")

            itemQuan.innerText = `x ${object.value}`
            itemPri.innerText = (productPrice * object.value).toString()
                .replace(/\B(?=(\d{3})+(?!\d))/g, ',') + " VND"
            totalQuan.innerText = `x ${data.total_quantity}`
            totalPri.innerText = (data.total_price).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',') + " VND"
            updateNumberCart(data.total_quantity)
        }
    }).catch(function (err) {
        console.log(err)
    })
}

function updateNumberCart(quantity) {
    let numberCart = document.getElementById("quantity-cart")
    numberCart.innerText = quantity
}

