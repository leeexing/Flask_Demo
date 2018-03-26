console.groupCollapsed('我会告诉你什么')
console.log('模块：用户名')
console.log('功能：获取用户信息')
console.log('方式：get、post')
console.log('地址：http://localhost:5002/page/users')
console.groupEnd()

const user_btn = document.querySelector('.users')

user_btn.onclick = e => {
  query('http://localhost:5002/page/users')
    .then(data => {
      console.log(data)
    })
}

function query(url, method='get', data=null){
  return new Promise((resolve, reject) => {
    let xhr = new XMLHttpRequest()
    xhr.open(method, url, true)
    xhr.onload = function() {
      if (this.status === 200) {
        resolve(this.response)
      }
    }
    xhr.onerror = function(e) {
      reject(e)
    }
    xhr.send(data)
  })
}
