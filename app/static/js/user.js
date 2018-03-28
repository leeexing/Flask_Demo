console.groupCollapsed('我会告诉你什么')
console.log('模块：用户名')
console.log('功能：获取用户信息')
console.log('方式：get、post')
console.log('地址：http://localhost:5002/page/users')
console.groupEnd()

const user_btn = document.querySelector('.users')
const user_wrap = document.querySelector('.user-wrap')

user_btn.onclick = e => {
  query('http://localhost:5002/page/users')
    .then(data => {
      console.log(data)
      showUsers(data)
    })
}

function showUsers(data) {
  let html = '<ul>'
  data.data.forEach(item => {
    html += `<li>用户名：${item.username}, 密码：${item.password}</li>`
  })
  html += '</ul>'
  user_wrap.innerHTML = html
}