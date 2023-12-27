const BASE_URL = 'http://127.0.0.1:80'  // адрес для отправки запросов на api

function saveToken(data){  // сохранение токена

    document.cookie=`access_token=${data.access_token}; path=/;`
}


function handleUserCredentials(data, id_to_red="") {  // Проверка введенных данных
    if (data.token){
        saveToken(data.token)
        window.location.replace('/')
    } else {
        //Data = new Date()
        //var hours_now = Data.getHours();
        //var minutes_now = Data.getMinutes();
            // Get the snackbar DIV
        var x = document.getElementById("snackbar");

        if (id_to_red){
            var field_to_red = document.getElementById("_" + id_to_red);
            field_to_red.style.borderColor = "red";
        }

        // Add the "show" class to DIV
        x.className = "show";
        x.textContent = data;

        // After 3 seconds, remove the show class from DIV
        setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
        //$("body").append(`<div class="position-fixed bottom-0 end-0 p-3" style="z-index: 5"><div id="liveToast" class="toast show" role="alert" aria-live="assertive" aria-atomic="true">   <div class="toast-header"> <strong class="me-auto">Будьте внимательнее</strong>  <small>${hours_now + ':' + minutes_now}</small> <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Закрыть"></button>   </div>  <div class="toast-body" style="color: red">${data}</div> </div> </div>`)

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
            error: function (error) {
                handleUserCredentials(error.responseJSON.detail)
                console.log(error.responseJSON.detail);
            },

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
      let border = document.querySelectorAll('input');
      for( let i = 0; i < border.length; i++ ){
         border[i].style.borderColor = "#CACACA";
      }

    //var phone = document.getElementById('country_code').value + document.getElementById('phone').value;
    var password = document.getElementById('_password').value
    var first_name = document.getElementById('_first_name').value;
    var last_name = document.getElementById('_last_name').value
    var email = document.getElementById('_email').value;
    //console.log(email + first_name + last_name + password)
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
            error: function (error) {
                handleUserCredentials(error.responseJSON.detail[0].msg, error.responseJSON.detail[0].loc[1])
                }

        }
    )
}


$('#sign_up').on('click', sendRegistrationData)
$('#sign_in').on('click', sendLoginData)