function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

async function delete_post(media_id, redirect_link) {
    /* Delete the given Media object and returns to the previous page. */
    var delete_confirm = confirm("Are you sure you want to delete this post?");
    
    if (delete_confirm) {
        var response = await fetch(media_id, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'type': 'delete_media',
                'media_id': media_id
            })
        }
        )
        window.location.assign(redirect_link)
        window.location.reload
    }
}
