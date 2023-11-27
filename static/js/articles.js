function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function ajax_like(article_url, like) {
    // создаем AJAX-вызов
    $.ajax({
        headers: {"X-CSRFToken": getCookie("csrftoken")},
        url: article_url + "like/",
        type: 'POST',
        data: {'like_or_dislike': like},
        // если успешно, то
        success: function (response) {
            $("#count_like").text(response.count_like);
            $("#count_dislike").text(response.count_dislike);
            if (like === 1) {
                $("#icon-like").toggleClass("bi-hand-thumbs-up bi-hand-thumbs-up-fill");
                if ($("#icon-dislike").hasClass("bi-hand-thumbs-down-fill")) {
                    $("#icon-dislike").toggleClass("bi-hand-thumbs-down bi-hand-thumbs-down-fill");
                }
            } else {
                $("#icon-dislike").toggleClass("bi-hand-thumbs-down bi-hand-thumbs-down-fill");
                if ($("#icon-like").hasClass("bi-hand-thumbs-up-fill")) {
                    $("#icon-like").toggleClass("bi-hand-thumbs-up bi-hand-thumbs-up-fill");
                }
            }
        },
        // если ошибка, то
        error: function (response) {
            // предупредим об ошибке
            get_alert(response.responseJSON.errors, "warning")
            console.log(response.responseJSON.errors)
        }
    });
    return false;
}

function ajax_like_comment(article_url, comment_id, like) {
    // создаем AJAX-вызов
    $.ajax({
        headers: {"X-CSRFToken": getCookie("csrftoken")},
        url: article_url + "like_comment/",
        type: 'POST',
        data: {"comment_id": comment_id.split('-')[1], 'like_or_dislike': like},
        // если успешно, то
        success: function (response) {
            $('#comments-container').load(article_url + 'show_comments/');
        },
        // если ошибка, то
        error: function (response) {
            // предупредим об ошибке
            get_alert(response.responseJSON.errors, "warning")
            console.log(response.responseJSON.errors);
        }
    });
    return false;
}

function ajax_post_comment(article_url, parent_comment, comment_area) {
    // создаем AJAX-вызов
    $.ajax({
        headers: {"X-CSRFToken": getCookie("csrftoken")},
        url: article_url + "add_comment/",
        type: 'POST',
        data: {'parent_comment': parent_comment, 'comment_area': comment_area},
        // если успешно, то
        success: function (response) {
            $('#comments-container').load(article_url + 'show_comments/');
        },
        // если ошибка, то
        error: function (response) {
            // предупредим об ошибке
            get_alert(response.responseJSON.errors, "warning")
            console.log(response.responseJSON.errors)
        }
    });
    return false;
}

function ajax_post_complaint(article_url, type_complaint) {
    // создаем AJAX-вызов
    $.ajax({
        headers: {"X-CSRFToken": getCookie("csrftoken")},
        url: article_url + "add_complaint/",
        type: 'POST',
        data: {type_complaint},
        // если успешно, то
        success: function (response) {
            get_alert("Жалоба успешно отправлена", "success")
        },
        // если ошибка, то
        error: function (response) {
            // предупредим об ошибке
            get_alert(response.responseJSON.errors, "warning")
            console.log(response.responseJSON.errors)
        }
    });
    return false;
}