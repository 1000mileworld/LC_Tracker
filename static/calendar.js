// default message for no problems changed in evo-calendar.js
// dot color changed in style in problem_list.html
// Initialize evo-calendar in your script file or an inline <script> tag
var calendarData = [];
var id_link_map = {};
for (const problem of my_problems) {
    calendarData.push({
        id: problem['id'],
        name: problem['title'],
        description: `#${problem['number']} - ${problem['difficulty']}`,
        date: problem['last_solved'],
        type: problem['difficulty'].toLowerCase()
    })
    id_link_map[problem['id']] = problem['link']
}

$(document).ready(function() {
    //settings
    $('#calendar').evoCalendar({
        'firstDayOfWeek': 0,
        'theme': 'Midnight Blue',
        'todayHighlight': true
    })
    $('#calendar').evoCalendar('addCalendarEvent', calendarData)

    // selectEvent
    $('#calendar').on('selectEvent', function(event, activeEvent) {       
        window.open(
            id_link_map[activeEvent['id']],
            '_blank'
        );
        // let a= document.createElement('a');
        // a.target= '_blank';
        // a.href= id_link_map[activeEvent['id']];
        // a.click();
        // a.remove();

        location.href = `confirm-redo/${activeEvent['id']}`
    });
})    