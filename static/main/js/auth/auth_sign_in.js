const BASE_URL = 'https://belcv.ru'
//const BASE_URL = 'http://127.0.0.1:8000'  // адрес для отправки запросов на api

function saveToken(data){

    document.cookie=`access_token=${data.access_token}; path=/;`
}

function handleUserCredentials(data) {
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

function deleteAllCookies() {
    var cookies = document.cookie.split(";");

    for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i];
        var eqPos = cookie.indexOf("=");
        var name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
        document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/;";
    }
} 

function sendLoginData(e) {

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

function handleTokenResponse(data){
    if (!data) {
        window.location.replace('/')
    } else {
        deleteAllCookies()
    }
}

function isUserAuth () {
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



// isUserAuth()
$('#sign_in').on('click', sendLoginData)
