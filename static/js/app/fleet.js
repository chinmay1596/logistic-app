let new_driver = null;
let driver_name = $('#driver-name');
let from_date = $('#from-date');
let previous_driver = $('#previous-driver');
let add_information = $('#add-information');

$('#id_drivers').on('change', function () {
    let id = $(this).val();
    $.get(
        `/employee/driver/${id}/json`,
        function (response) {
            new_driver = response;
            $('#driver_status').val(response.status);
            $('#vehicle_type').val(response.vehicle_type);
        }
    )
})

function convertDate(date) {
    let d = new Date(date);

    let month = d.getMonth() + 1;
    let day = d.getDate();

    return (month < 10 ? '0' : '') + month + '/' + (day < 10 ? '0' : '') + day + '/' + d.getFullYear();
}

function successFormSubmit(data) {
    let response = JSON.parse(data.instance)[0];

    if (driver_name.text() !== 'N/A') {
        $('#empty-driver-view').remove();
        let previous_driver = {
            "driver": {
                "full_name": driver_name.text()
            },
            "from_date": from_date.text(),
            "to_date": convertDate(new Date())
        }
        fillPreviousDriver(previous_driver);
    }

    driver_name.html(`${new_driver.user.full_name}`);
    from_date.html(`${convertDate(response.fields.from_date)}`);
}

function fillPreviousDriver(data) {
    previous_driver.prepend(
        `
            <div class="tr">
                <span>${convertDate(data.from_date)} - ${convertDate(data.to_date)}</span>
                <div class="row">${data.driver.full_name}</div>
            </div>
        `
    )
}

$.get(
    previous_driver.attr('url'),
    function (data) {
        if (data.results.length > 0) {
            $.each(data.results, function (index, value) {
                fillPreviousDriver(value)
            })
        } else {
            previous_driver.prepend(
                `
                    <div class="tr" id="empty-driver-view">
                        <small>N/A</small>
                    </div>
                `
            )
        }
    }
)
