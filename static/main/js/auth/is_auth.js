const BASE_URL = 'https://belcv.ru'
const login_url = BASE_URL + '/auth/login'


function deleteAllCookies() {
    var cookies = document.cookie.split(";");

    for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i];
        var eqPos = cookie.indexOf("=");
        var name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
        document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/;";
    }
} 

function logOut() {
    deleteAllCookies()
    window.location.replace('/login')
}

$('#logout').on('click', logOut)