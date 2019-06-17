$(document).ready(() => {
    // Genre adding modal dialog
    const docEl = $(document.documentElement);

    const genreAddModal = $('#genre-add-modal');
    const studioAddModal = $('#studio-add-modal');

    const genreModalInputField = $('#genre-new-input');
    const studioModalInputField = $('#studio-new-input');

    // Genre modal dialog
    $('#genre-add-button').click(() => {
        docEl.addClass('is-clipped');
        genreAddModal.addClass('is-active');
        genreModalInputField.val($('#genre-search-field').val());
        return false;
    });
    $('#genre-new-create-button').click(() => {
        $.ajax({
            type: 'POST',
            url: '/movies/genres/create/',
            data: {
                title: genreModalInputField.val()
            },
            success: (data, status) => {
                if (data !== 'False') {
                    let parsedData = data.split(',');
                    $(`<option value="${parsedData[0]}">${parsedData[1]}</option>`).insertBefore('#genre-hold');
                    genreAddModal.removeClass('is-active');
                    docEl.removeClass('is-clipped');
                } else {
                    $('#genre-modal-notification').show().append(
                        `<div class="notification is-primary" id="genre-ntf" style="margin-bottom: 10px;">
                            <button class="delete" id="genre-delete-ntf"></button>
                            This genre already exist. Please use search form!
                        </div>`
                    );
                    $('#genre-delete-ntf').click(() => {
                        $('#genre-ntf').remove();
                        $('#genre-modal-notification').hide();
                    });
                }
            },
            error: (xhr, status, e) => {
            }
        });
        return false;
    });

    // Studio modal dialog
    $('#studio-add-button').click(() => {
        docEl.addClass('is-clipped');
        studioAddModal.addClass('is-active');
        return false;
    });
    $('#studio-new-create-button').click(() => {
        $.ajax({
            type: 'POST',
            url: '/movies/studios/create/',
            data: {
                name: studioModalInputField.val()
            },
            success: (data, status) => {
                if (data !== 'False') {
                    let parsedData = data.split(',');
                    $('#id_studio').append(`<option value="${parsedData[0]}">${parsedData[1]}</option>`);
                    studioAddModal.removeClass('is-active');
                    docEl.removeClass('is-clipped');
                } else {
                    $('#studio-modal-notification').show().append(
                        `<div class="notification is-primary" id="studio-ntf" style="margin-bottom: 10px;">
                            <button class="delete" id="studio-delete-ntf"></button>
                            This studio already exist. Please use search form!
                        </div>`
                    );
                    $('#studio-delete-ntf').click(() => {
                        $('#studio-ntf').remove();
                        $('#studio-modal-notification').hide();
                    });
                }
            },
            error: (xhr, status, e) => {
            }
        });
        return false;
    });

    // Handle modal close event
    $('.modal-close').click(() => {
        genreAddModal.removeClass('is-active');
        studioAddModal.removeClass('is-active');
        docEl.removeClass('is-clipped');
        return false;
    });

    // Genres filter
    const genreSelect = $('#id_genre > option').toArray();

    $('#id_genre').append(`<option disabled style="display: none;" id="genre-hold">Nothing to show...</option>`);
    $('#genre-search-field').on('input', (el) => {
        let input = $(el.target).val().toLowerCase();
        genreSelect.filter(genre => {
            if (genre.text.toLowerCase().includes(input)) {
                $(genre).show();
                $('#genre-hold').hide();
            } else {
                $(genre).hide();
                $('#genre-hold').show();
            }
        });
        return false;
    });

    // Related filter
    const relatedSelect = $('#id_related > option').toArray();

    $('#id_related').append(`<option disabled style="display: none;" id="related-hold">Nothing to show...</option>`);
    $('#related-search-field').on('input', (el) => {
        let input = $(el.target).val().toLowerCase();
        relatedSelect.filter(related => {
            if (related.text.toLowerCase().includes(input)) {
                $(related).show();
                $('#related-hold').hide();
            } else {
                $(related).hide();
                $('#related-hold').show();
            }
        });
        return false;
    });
});