function handleResponseCommentData (new_comment_data) {
    var list_of_comments = document.getElementById('comments');
    var li = `<li class="comment"><div class="comment-body"><h3>${new_comment_data["name"]}</h3><div class="meta">${new_comment_data["date_creation"]}</div><p>${new_comment_data["text"]}</p></div></li>`
//    console.log(new_comment_data)
    list_of_comments.insertAdjacentHTML('beforeend', li)
}

function handleResponseNewPostData (new_post_data) {
    location.reload()
}

function handleUserCredentials(data, id_to_red="") {  // Проверка введенных данных
    console.log(data)
    if (data.token){
        saveToken(data.token)
        window.location.replace('/')
    } else {
            // Get the snackbar DIV
        var x = document.getElementById("snackbar");

        if (id_to_red){
            var field_to_red = document.getElementById(id_to_red);
            field_to_red.style.borderColor = "red";
        }

        // Add the "show" class to DIV
        x.className = "show";
        x.textContent = data;

        // After 3 seconds, remove the show class from DIV
        setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);

    }
}


function sendCommentData(e) {

        const currentUrl = window.location.href.split('/');

        e.preventDefault()
        var name = document.getElementById('name').value
        var email = document.getElementById('email').value;
        var text = document.getElementById('message').value
        var post_id = document.getElementById('post-id').value
//        console.log(name, email, text)

        $.ajax(
        {
            url: BASE_URL + '/api/v1/posts/' + currentUrl[4] + '/' + currentUrl[5],
            method: 'post',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({
                'name': name,
                'email': email,
                'text': text,
                'post_id': post_id
            }),
            success: handleResponseCommentData,
            error: function (error) {
                console.log(error)
                }

        }
        )
}

function sendNewPostData(e) {
        e.preventDefault()

        const currentUrl = window.location.href.split('/');

        var title = document.getElementById('title').value
        var text = document.getElementById('text').value;
        var short_description = document.getElementById('short-description').value
        var category_id = document.getElementById('category-id').value

        $.ajax(
        {
            url: BASE_URL + '/api/v1/add-post',
            method: 'post',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({
                'title': title,
                'text': text,
                'short_description': short_description,
                'category_id': category_id
            }),
            success: handleResponseNewPostData,
            error: function (error) {
                if (error.responseJSON.detail[0].msg) {
                    handleUserCredentials(error.responseJSON.detail[0].msg, error.responseJSON.detail[0].loc[1])
                    }
                else {
                    handleUserCredentials(error.responseJSON.detail)
                    }
                }

        }
        )
}



$('#leave-comment').on('click', sendCommentData)
$('#add-post').on('click', sendNewPostData)