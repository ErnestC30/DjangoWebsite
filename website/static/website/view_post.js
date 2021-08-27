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

async function delete_post(media_id, redirect_link) {
    console.log(redirect_link)
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
