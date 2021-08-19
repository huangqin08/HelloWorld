// 刷新数据 
// chart 承载模块 // data 代表需要改变数据体

function refreshDatas (chart, data) {
    var index = 0;
    var timer = setInterval(function() {
        if (index < data.length) {
            refreshData(chart, data[index])
            index++;
        } else {
            clearInterval(timer)
            refreshDatas(chart, data);
        }
    }, 3000);

    function refreshData(chart,data){
        var itemData = data;
        var option = chart.getOption();
        if (data.xAxis) option.xAxis[0].data = data.xAxis;
        if (data.yAxis) option.yAxis[0].data = data.yAxis;
        if (data.series) itemData = data.series;
        for (var i = 0; i < itemData.length - 1; i++) {
            option.series[i].data = itemData[i];
        }
       
        chart.setOption(option);    
    }
}
