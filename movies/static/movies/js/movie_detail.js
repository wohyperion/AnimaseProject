$(document).ready(() => {
    $('#favorite-button').click((event) => {
        $.ajax({
            type: 'POST',
            url: document.URL + 'favorite/',
            success: (data, textStatus) => {
                if (data === 'False') {
                    $('#favorite-button').html('<a href="">Favorite</a>');
                    const favCount = $('#favorite-count');
                    favCount.text(favCount.text() - 1);
                } else {
                    $('#favorite-button').html('<a href="">Unfavorite</a>');
                    const favCount = $('#favorite-count');
                    favCount.text(+favCount.text() + 1);
                }
            },
            error: (xhr, status, e) => {
                if (e === 'Forbidden') {
                    $('#main-content').parent().prepend(
                        `
                            <div class="notification is-primary" id="login-ntf">
                                <button class="delete" id="delete-ntf"></button>
                                Please <a href="/accounts/login/?next=/movies/">login</a> to save anime to your favorites list and leave feedback.
                            </div>
                        `
                    );

                    $('#delete-ntf').click(() => {
                        $('#login-ntf').remove()
                    });
                }
            }
        });
        return false;
    });
});
