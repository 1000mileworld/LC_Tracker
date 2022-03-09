// default message for no problems changed in evo-calendar.js
// dot color changed in style in problem_list.html
// Initialize evo-calendar in your script file or an inline <script> tag
var calendarData = [];
var id_link_map = {};
const d = new Date();
for (const problem of my_problems) {
    var parsed_date;
    if (problem['next_solve']){
        var problem_date = problem['next_solve'].split('-'); //strange 1 off error if using yyyy-mm-dd
        parsed_date = `${problem_date[1]}/${problem_date[2]}/${problem_date[0]}`
    }else{
        parsed_date = null
    }
    
    calendarData.push({
        id: problem['id'],
        name: problem['title'],
        description: `#${problem['number']} - ${problem['difficulty']}`,
        date: parsed_date,
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