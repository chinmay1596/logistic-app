
var user_id = document.getElementById("records_table").getAttribute("url");
var csrf_token = document.getElementById("records_table").getAttribute("content");

function convertDate(date) {
    let d = new Date(date);

    let month = d.getMonth() + 1;
    let day = d.getDate();

    return (month < 10 ? '0' : '') + month + '/' + (day < 10 ? '0' : '') + day + '/' + d.getFullYear();
}


$.ajax({
    url: `/notification/show_notification/${user_id}/`,
    type: 'GET',
    success: function (data)
    {
        document.getElementById('notification_count').innerHTML=data.notification_count
        var notification;
        var append_html = '';
        if (data.results.length > 3)
        {
            document.getElementById("records_table").setAttribute("style","height: 400px;overflow: auto;");

        }
        if (data.results.length > 0)
        {
            for (notification = 0; notification < data.results.length; notification++)
            {
                if(data.results[notification].read==true)
                {
                    append_html += `<div class="notificationItem" style="background:#e3e3e37a;">`
                }
                else
                {
                    append_html += `<div class="notificationItem">`
                }
            append_html +=
            `
                <div class="toptitle">
                    <div class="image">
                        <a href=` + data.results[notification].click_action + `><img src="/static/assets/notification-user.svg" alt=""></a>
                    </div>
                    <div class="content">
                        <a href=` + data.results[notification].click_action + `><h4 id="notification_title">` + data.results[notification].title + `</h4></a>
                        <p id="notification_date">` + convertDate(data.results[notification].created_at) + `</p>
                 </div>
                </div>
                <div class="mainContent">
                    <p id="notification_msg">
                        ` + data.results[notification].message + `
                    </p>
                </div>
                    <div class="notifications-checkbox">
                     <label class="checkboxCustom">
                        <span class="checkbox__input" id="markNotifications">
                         `
                        if(data.results[notification].read==true)
                        {
                          append_html +=
                          `
                          <input type="checkbox" class="notification_check" id="not_checkbox" name="checkbox" value=` + data.results[notification].id + ` checked >`
                        }
                        else
                        {
                         append_html +=
                              `<input type="checkbox" class="notification_check" id="not_checkbox" name="checkbox" value=` + data.results[notification].id + ` >`
                         }
                         append_html +=
                         `
                          <span class="checkbox__control">
                            <svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' aria-hidden="true" focusable="false">
                              <path fill='none' stroke='currentColor' stroke-width='3' d='M1.73 12.91l6.37 6.37L22.79 4.59' /></svg>
                          </span>
                          <span class="radio__label">Read</span>
                        </span>
                      </label>
                    </div>
                </div>
                `
            }
        }
        else
        {
        append_html +=
            `
            <div class="notificationItem">
                <div class="nonotification_content text-center">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 13h6M3 17V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2z"></path></svg>
                    <h4>No notifications found</h4>
                </div>
            </div>
            `
        }
        $('#records_table').append(append_html);
    }
});

$(document).ready(function()
{
    $(document).on('change','#not_checkbox',function()
    {
        var notification_id=$(this).attr('value');

        if (this.checked)
        {
            var read = 'True'
            $(this).closest('.notificationItem').css( "background", "#e3e3e37a" );
        }
        else
        {
            var read = 'False'
            $(this).closest('.notificationItem').css( "background", "white" );
        }
        $.ajax({
            data: {
                "notification_id": notification_id,
                "read": read,
                csrfmiddlewaretoken: csrf_token,
            },
            type: "post",
            url: `/notification/mark_notification/${notification_id}/`,
            success: function(data)
            {
                 document.getElementById('notification_count').innerHTML=data.notification_count
            },
        });
    });
});
