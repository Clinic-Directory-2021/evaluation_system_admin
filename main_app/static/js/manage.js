var current_id_var;
function add_seminar(){
    window.location.href = '../add_seminar/';
}
function add_facilitator(){
    window.location.href = '../add_facilitator/';
}
function add_evaluator(){
    window.location.href = '../add_evaluator/';
}
function edit_seminar(variable){
    window.location.href = '../edit_seminar?current_id=' + variable;
}
function edit_facilitator(variable){
    window.location.href = '../edit_facilitator?current_id=' + variable;
}
function edit_evaluator(variable){
    window.location.href = '../edit_evaluator?current_id=' + variable;
}
function view_evaluator(variable){
    window.location.href = '../edit_evaluator?current_id=' + variable;
}
function export_evaluation(){
    window.location.href = '../export_evaluator/';
}
function delete_seminar(){
    window.location.href = '../delete_seminar?current_id=' +  current_id_var;
}
// function delete_facilitator(variable){
//     window.location.href = '../delete_facilitator?current_id=' + variable;
// }
function delete_evaluator(){
    window.location.href = '../delete_evaluator?current_id=' + current_id_var;
}

function current_id(variable){
    current_id_var = variable
}