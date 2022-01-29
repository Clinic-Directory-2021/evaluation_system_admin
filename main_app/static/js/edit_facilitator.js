var facilitator_name
var position
var topic 
var start_time 
var end_time
var facilitator_id
function set_facilitator_data(facilitator_name, position, topic, start_time, end_time, facilitator_id) {

        this.facilitator_name = facilitator_name
        this.position = position
        this.topic = topic
        this.start_time = start_time
        this.end_time = end_time
        this.facilitator_id = facilitator_id

        $('#edit_facilitator_name').val(get_facilitator_name())
        $('#edit_position').val(get_position())
        $('#edit_topic').val(get_topic())
        $('#edit_start_time').val(get_start_time())
        $('#edit_end_time').val(get_end_time())


}
function get_facilitator_name(){
    return facilitator_name
}
function get_position(){
    return position
}
function get_topic(){
    return topic
}
function get_start_time(){
    return start_time
}
function get_end_time(){
    return end_time
}
function get_facilitator_id(){
    return facilitator_id
}

function save_changes(){
    window.location.href = "/post_edit_facilitator?facilitator_id="+get_facilitator_id()+"&position="+$('#edit_position').val()+"&facilitator_name="+$('#edit_facilitator_name').val()+"&topic="+$('#edit_topic').val()+"&start_time="+$('#edit_start_time').val()+"&end_time="+$('#edit_end_time').val();
}