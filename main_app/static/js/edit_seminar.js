var facilitator_id;
function delete_facilitator(){
    window.location.href = "/post_delete_facilitator?facilitator_id="+get_facilitator_id()
}
function set_facilitator_id(facilitator_id){
    this.facilitator_id = facilitator_id
}
function get_facilitator_id(){
    return facilitator_id
}