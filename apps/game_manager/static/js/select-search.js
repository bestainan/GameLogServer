    $(document).ready(function(){

        //华丽初始化
        $(".chzn-select").chosen();

        //单选select 数据同步
        chose_get_ini('#dl_chose');
        //change 事件
        $('#dl_chose').change(function(){
                alert(chose_get_value('#dl_chose') + ' : '+ chose_get_text('#dl_chose'));
        });

        //多选select 数据同步
        chose_get_ini('#dl_chose2');
        //change 事件
        $('#dl_chose2').change(function(){
            alert(chose_get_value('#dl_chose2') + ' : '+ chose_get_text('#dl_chose2'));
        });

    });

    //select 数据同步
    function chose_get_ini(select){
        $(select).chosen().change(function(){$(select).trigger("liszt:updated");});
    }
    //单选select 数据初始化
    function chose_set_ini(select, value){
        $(select).attr('value',value);
        $(select).trigger("liszt:updated");
    }
    //单选select value获取
    function chose_get_value(select){
        return $(select).val();
    }
    //select text获取，多选时请注意
    function chose_get_text(select){
        return $(select+" option:selected").text();
    }

    //多选select 数据初始化
    function chose_mult_set_ini(select, values){
        var arr = values.split(',');
        var length = arr.length;
        var value = '';
        for(i=0;i<length;i++){
            value = arr[i];
            $(select+" [value='"+value+"']").attr('selected','selected');
        }
        $(select).trigger("liszt:updated");
    }
