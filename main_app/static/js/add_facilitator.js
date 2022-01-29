var ctr = 1;
var facilitator_list_holder = "";
function add_facilitators(){
  var position = $('#position').val();
    var facilitator_name = $('#facilitator_name').val();
    var topic = $('#topic').val();
    var start_time = time_converter($('#start_time').val());
    var end_time = time_converter($('#end_time').val());
    
    if(facilitator_name == "" || position == "" || topic == "" || start_time == "Invalid Date" || end_time == "Invalid Date"){
      swal({
        title: "Error.",
        text: "All fields are required",
        icon: "error",
        button: "Okay",
      });
      $('#facilitator_name').val("");
      $('#position').val("");
    $('#topic').val("");
    $('#start_time').val("");
    $('#end_time').val("");
    }
    else{

    
    $('#output').append("<tr><td>"+ctr+"</td><td>"+facilitator_name+"</td><td>"+position+"</td><td>"+topic+"</td><td>"+start_time+"</td><td>"+end_time+"</td>"
    +"<td><button class='button success'\
    data-role='hint'\
    data-hint-position='top'\
    data-hint-text='Edit Facilitator Data'\
    data-cls-hint='bg-green fg-white drop-shadow' name='edit_button' disabled>Edit</button>\
    <button class='button alert'\
    data-role='hint'\
    data-hint-position='top'\
    data-hint-text='Remove facilitator in list table'\
    data-cls-hint='bg-red fg-white drop-shadow' name='remove_button' onclick='Metro.dialog.open('#delete_dialog'), set_facilitator_id('{{facilitator_data.facilitator_id}}')\" disabled>Remove</button><br> <p style='font-size:12px;' '>(You Need To Save Changes to use use this Actions)<p></td></tr>");
    facilitator_list_holder += facilitator_name + "=" + position+ "=" + topic + "=" +  start_time + "-" + end_time + ";"
    $('#facilitator_list').val(facilitator_list_holder)
    // alert($('#facilitator_list').val());
    ctr++;

    $('#facilitator_name').val("");
    $('#position').val("");
    $('#topic').val("");
    $('#start_time').val("");
    $('#end_time').val("");
  }
}

function close_add_modal(){
  $('#facilitator_name').val("");
  $('#position').val("");
  $('#topic').val("");
  $('#start_time').val("");
  $('#end_time').val("");
}

function time_converter(time){
    const timeString12hr = new Date('1970-01-01T' + time + 'Z')
    .toLocaleTimeString('en-US',
      {timeZone:'UTC',hour12:true,hour:'numeric',minute:'numeric'}
    );

    return timeString12hr;
}

function clear_list(){
  facilitator_list_holder = "";
  $('#facilitator_list').val(facilitator_list_holder)
  $('#output').html(" ");
}

function clear_changes(){
window.location.reload()
}

function validate_facilitator(){
  if(facilitator_list_holder == "")
    $('#validation').val("no")
  else
   $('#validation').val("yes")
  }