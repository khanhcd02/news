// Function to update current date and time with day of the week
function updateDateTime() {
    var daysOfWeek = ["Chủ nhật", "Thứ hai", "Thứ ba", "Thứ tư", "Thứ năm", "Thú sáu", "Thứ bảy"];
    var currentDate = new Date();

    var dayOfWeek = daysOfWeek[currentDate.getDay()];
    var day = currentDate.getDate();
    var month = currentDate.getMonth() + 1; // Months are zero based
    var year = currentDate.getFullYear();

    var hours = currentDate.getHours();
    var minutes = currentDate.getMinutes();
    var seconds = currentDate.getSeconds();

    // Add leading zeros if necessary
    month = (month < 10 ? "0" : "") + month;
    day = (day < 10 ? "0" : "") + day;
    hours = (hours < 10 ? "0" : "") + hours;
    minutes = (minutes < 10 ? "0" : "") + minutes;
    seconds = (seconds < 10 ? "0" : "") + seconds;

    // Assemble the string
    var dateTimeString = dayOfWeek + ", " + day + "/" + month + "/" + year + " " + hours + ":" + minutes + ":" + seconds;

    // Update the paragraph element with the current date and time with day of the week
    document.getElementById("datetime").innerText = dateTimeString;
}

// Update the date and time immediately
updateDateTime();

// Update the date and time every second
setInterval(updateDateTime, 1000);