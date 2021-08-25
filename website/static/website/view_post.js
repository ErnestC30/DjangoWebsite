function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

function delete_post(url, media_id, redirect_link) {
    var delete_confirm = confirm("Are you sure you want to delete this post?");
    console.log(redirect_link)
    if (delete_confirm) {
        fetch(media_id, {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            body: JSON.stringify({'type': 'delete_post',
                                  'media_id': media_id}) 
            }
        )
        .then(response => response)
        .then(window.location.replace(redirect_link))
        .catch(error => console.log(error))
    }
}