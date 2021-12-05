function month_filter() {
    var month = document.getElementsByClassName('month')
    var checkValue = []
    for (var i = 0; i < month.length; i++) {
        if (month[i].checked)
            checkValue.push(i + 1)
    }
    fetch('/admin/statsview/', {
        'method': 'post',
        'body': JSON.stringify({
            'checkValue': checkValue
        }),
        'headers': {
            'Content-Type': 'application/json'
        }
    })
}