$(document).ready(function(){
    $('.chk input').on('change',function(){
        var value = $(this).parent('td').prev('td').html();
        console.log(value)
        value = parseInt(value);
        if(this.checked) {
            $("#amount").html( parseInt($("#amount").html()) + value );
        }
        else {
            $("#amount").html( parseInt($("#amount").html()) - value );
        }
    });

    $('#selectAll').click(function(e){
        var table= $(e.target).closest('table');
        $('td input:checkbox',table).prop('checked',this.checked);
    });

    $('#selectAll1').click(function(e){
        var table= $(e.target).closest('table');
        $('td input:checkbox',table).prop('checked',this.checked);
    });
});

