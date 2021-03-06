$(document).ready(function(){

    //BEGIN toggle bar with tucked menu
    document.getElementById('toggle').addEventListener('click', function(e){
        document.getElementById('tuckedMenu').classList.toggle('custom-menu-tucked');
        document.getElementById('toggle').classList.toggle('x');
    });
    //END toggle bar with tucked menu

    $(window.id_fecha_liquidacion).prop('min',$(window.id_fecha_inicio).val());
    $(window.id_fecha_finalizacion).prop('min',$(window.id_fecha_inicio).val());
    $(window.id_fecha_inicio).prop('max',$(window.id_fecha_finalizacion).val());


    $(window.id_fecha_inicio, this).on('change',function(){
    /* this is used to correct if the user puts a enddate before the startdate */
        var fechaInicio = new Date($(window.id_fecha_inicio).val());
        var fechaLiquidacion = new Date($(window.id_fecha_liquidacion).val());
        if (fechaInicio > fechaLiquidacion){
            $(window.id_fecha_liquidacion).val($(this).val());
            $(window.id_fecha_finalizacion).val($(this).val());
        }
        $(window.id_fecha_liquidacion).prop('min',$(this).val());
        $(window.id_fecha_finalizacion).prop('min',$(this).val());

    });

        $(window.id_fecha_liquidacion, this).on('change',function(){
    /* the liquidation day must be same or after  finalization day */
            $(window.id_fecha_finalizacion).val($(this).val());
    });

    $(window.id_fecha_finalizacion).blur(function(){
    /* the liquidation day must be same or after  finalization day */
        var fechaFinalizacion = new Date($(window.id_fecha_finalizacion).val());
        var fechaLiquidacion = new Date($(window.id_fecha_liquidacion).val());
        if (fechaFinalizacion >= fechaLiquidacion){
            $(window.id_demanda_salarios_caidos).prop('disabled',true);
        }
        else if (fechaFinalizacion < fechaLiquidacion){
            $(window.id_demanda_salarios_caidos).prop('disabled',false);
            $(window.id_demanda_salarios_caidos).removeProp('disabled');
        }
    });


    $(window.id_clase_contrato, this).on('change', function(){
    /* this is because  the end date is not used in indefinited contract
        we put  read only and change its value at same time that fecha liquidacion*/
        var isIndefinido = ($(this).val() == 'ind');
        if (isIndefinido) {

            $(window.id_fecha_finalizacion).prop('readonly',true);
            $(window.id_fecha_liquidacion, this).on('change', function(){
                $(window.id_fecha_finalizacion).val($(this).val());
            });
        }
        else{

            $(window.id_fecha_finalizacion).prop('readonly',false);
            $(window.id_fecha_finalizacion).removeProp('readonly');
        }
    });


});


