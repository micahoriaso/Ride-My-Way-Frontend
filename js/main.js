function friendlyDate(date){
    friendly_date = new Date(date)
    return friendly_date.toDateString()
}

function friendlyTime(time){
    friendly_time = new Date('1970-01-01T' + time)
    return friendly_time.toLocaleTimeString()
}