console.groupCollapsed('你想知道什么')
console.log('姓名：李星')
console.log('职业：web前端工程师')
console.log('爱好：篮球、户外、逛街')
console.log('个人网站：http://www.leeeing.com/')
console.groupEnd()


/**
 * 
 * @param {*} files 
 */
function upload(files) {
  console.log(files)
  let formData = new FormData()
  let xhr = new XMLHttpRequest()
  Array.from(files).forEach(file => {
    formData.append('fileName', file)
  })
  return formData
  // formData.set('fileName', files)
  // xhr.open('POST', '/upload', true)
  // xhr.onreadystatechange =function() {
  //   if (xhr.readyState == 4 && xhr.status === 200) {
  //     console.log(this.response)
  //   }
  // }
  // xhr.onerror = e => {
  //   console.error(e)
  // }
  // xhr.send(formData)
}

/**
 * 原生js封装请求
 * @param {*} url 
 * @param {*} method 
 * @param {*} data 
 */
function query(url, method='get', data=null){
  return new Promise((resolve, reject) => {
    let xhr = new XMLHttpRequest()
    xhr.open(method, url, true)
    xhr.responseType = 'json'
    xhr.onload = function() {
      if (this.status === 200) {
        resolve(this.response)
      }
    }
    xhr.onerror = function(e) {
      reject(e)
    }
    // post 请求的数据需要格式化，不能直接传递 object 对象
    if (method !== 'get' && data) {
      data = postDataFormat(data)
      if (typeof FormData !== 'function') {
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded')
        // xhr.setRequestHeader('Content-Type', 'application/json')
      }
    }
    xhr.send(data)
  })
}

function postDataFormat(obj) {
  if (typeof FormData === 'function') {
    let formData = new FormData()
    Object.keys(obj).forEach(key => {
      formData.append(key, obj[key])
    })
    return formData
  } else {
    let arr = []
    Object.keys(obj).forEach(key => {
      arr.push(`${encodeURIComponent(key)}=${encodeURIComponent(obj[key])}`)
    })
    return arr.join('&')
  }
}

