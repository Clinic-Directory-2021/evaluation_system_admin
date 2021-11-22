var ctr = 1;
var facilitator_list_holder = "";
function add_facilitator(){
    var facilitator_name = $('#facilitator_name').val();
    var topic = $('#topic').val();
    var start_time = time_converter($('#start_time').val());
    var end_time = time_converter($('#end_time').val());
    
    $('#output').append("<tr><td>"+ctr+"</td><td>"+facilitator_name+"</td><td>"+topic+"</td><td>"+start_time+"</td><td>"+end_time+"</td></tr>");
    facilitator_list_holder += facilitator_name + "=" + topic + "=" +  start_time + "-" + end_time + ";"
    $('#facilitator_list').val(facilitator_list_holder)
    // alert($('#facilitator_list').val());
    ctr++;

    $('#facilitator_name').val("");
    ('#topic').val("");
    ('#start_time').val("");
    ('#end_time').val("");
}

function time_converter(time){
    const timeString12hr = new Date('1970-01-01T' + time + 'Z')
    .toLocaleTimeString('en-US',
      {timeZone:'UTC',hour12:true,hour:'numeric',minute:'numeric'}
    );

    return timeString12hr;
}

// ctr.toString() + ".Facilitator name: <u>"+ facilitator_name + "</u>" +" Time to Speak: <u>" + start_time + "-" + end_time +"</u>" + "<br>"