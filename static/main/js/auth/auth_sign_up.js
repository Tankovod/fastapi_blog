const BASE_URL = 'http://127.0.0.1:8000'  // адрес для отправки запросов на api

function saveToken(data){  // сохранение токена

    document.cookie=`access_token=${data.access_token}; path=/;`
}

function handleUserCredentials(data) {  // Проверка введенных данных
    if (data.token){
        saveToken(data.token)
        window.location.replace('/')
    } else {
        console.log(data.message)
        Data = new Date()
        var hours_now = Data.getHours();
        var minutes_now = Data.getMinutes();
        $("body").append(`<div class="position-fixed bottom-0 end-0 p-3" style="z-index: 5"><div id="liveToast" class="toast show" role="alert" aria-live="assertive" aria-atomic="true">   <div class="toast-header"> <strong class="me-auto">Bootstrap</strong>  <small>${hours_now + ':' + minutes_now}</small> <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Закрыть"></button>   </div>  <div class="toast-body" style="color: red">${data.message}</div> </div> </div>`)

    }
}

function deleteAllCookies() {  // удаление всех куков
    var cookies = document.cookie.split(";");

    for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i];
        var eqPos = cookie.indexOf("=");
        var name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
        document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/;";
    }
}

function sendLoginData(e) {  // Отправка формы авторизации

    e.preventDefault()
    var email = document.getElementById('email').value
    var password = document.getElementById('password').value
    $.ajax(
        {
            url: BASE_URL + '/api/v1/login',
            method: 'post',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({
                'email': email,
                'password': password
            }),
            success: handleUserCredentials,
            error: (x) => console.log(`Error: ${x}`),

        }
    )
}

function handleTokenResponse(data){  // если пользователь авторизован перенаправляет на глауную, в противном случае удаляет все куки
    if (!data) {
        window.location.replace('/')
    } else {
        deleteAllCookies()
    }
}

function isUserAuth () {  // Проверка авторизован ли пользователь
    console.log(document.cookie)
    if (document.cookie.includes("access_token")) {
        $.ajax(
            {
                url: BASE_URL + '/api/auth/token',
                method: 'post',
                dataType: 'json',
                contentType: 'application/json',
                data: JSON.stringify({
                    'access_token': document.cookie
                }),
                success: handleTokenResponse,
                error: (x) => console.log(`Error: ${x}`),

            }
        )
    }
}


function saveToken(data){  // Енпосредственно само сохранение
    document.cookie=`access_token=${data.access_token}; path=/;`
}

function handleUserData(data) {  // Сохранение токена и редирект
    console.log(`${data.message}`)
        saveToken(data.token)
        window.location.replace('/')
}


function sendRegistrationData(e) {  // Отправка формы регистрации
    e.preventDefault()
    //var phone = document.getElementById('country_code').value + document.getElementById('phone').value;
    var password = document.getElementById('_password').value
    var first_name = document.getElementById('_first_name').value;
    var last_name = document.getElementById('_last_name').value
    var email = document.getElementById('_email').value;
    console.log(email + first_name + last_name + password)
    $.ajax(
        {
            url: BASE_URL + '/api/v1/registration',
            method: 'post',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({
//                'phone': phone,
                'password': password,
                'first_name': first_name,
                'last_name': last_name,
                'email': email
            }),
            success: handleUserData,
            error: (x) => console.log(`ERROR: ${x}`),

        }
    )
}

$('#sign_up').on('click', sendRegistrationData)
$('#sign_in').on('click', sendLoginData)