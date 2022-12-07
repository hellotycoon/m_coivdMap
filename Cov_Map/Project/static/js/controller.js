function get_time() {
    $.ajax({
        url: "/time",
        timeout: 10000,
        success: function (data) {
            $(".showtime").html(data)
        },
        error: function () {
        }
    })
}
setInterval(get_time,500)
function get_total_data_of_china() {
    $.ajax({
        url: "/total_data_of_china",
        timeout: 10000,
        success: function (data) {
            $(".no-hd ul li").eq(0).text(data.currentConfirmedCount)
            $(".no-hd ul li").eq(1).text(data.suspectedCount)
            $(".no-hd ul li").eq(2).text(data.curedCount)
            $(".no-hd ul li").eq(3).text(data.deadCount)
        },
        error: function () {
        }
    })
}

function get_map_data() {
    $.ajax({
        url: 'china_map',
        success: function (data) {
            mapOption.series[0].data = data.data
            echartsMap.setOption(mapOption)
        },
        error: function () {
        }
    })
}
function get_wordcloud_data(){
    $.ajax({
        url:"/wordcloud",
        success:function (data){
            wordCloudOption.series[0].data=data.kws;
            ecWordCloud.setOption(wordCloudOption);
        },
       error: function () {
        }
    })
}
function get_top10_data(){
   $.ajax({
       url:"/cov_top10",
       success:function (data){
            ecCov_top10_option.xAxis.data = data.city;
            ecCov_top10_option.series[0].data=data.currentConfirmedCount;
            ecCov_top10.setOption(ecCov_top10_option);
      },
       error:function(){
       }
   })
}
function get_cov_trend_data(){
   $.ajax({
       url:"/cov_trend",
       success:function (data){
            ecMulti_line_option.xAxis.data = data.date;
            ecMulti_line_option.series[0].data=data.confirmedCount;
            ecMulti_line_option.series[1].data=data.currentConfirmedCount;
            ecMulti_line_option.series[2].data=data.suspectedCount;
            ecMulti_line_option.series[3].data=data.curedCount;
            ecMulti_line_option.series[4].data=data.deadCount;
            ecMulti_line.setOption(ecMulti_line_option);
      },
       error:function(){
       }
   })
}
function get_cov_trend_cq_data(){
   $.ajax({
       url:"/cov_trend_cq",
       success:function (data){
            ecMulti_line_cq_option.xAxis.data = data.date;
            ecMulti_line_cq_option.series[0].data=data.confirmedIncr;
            ecMulti_line_cq_option.series[1].data=data.currentConfirmedIncr;
            ecMulti_line_cq_option.series[2].data=data.suspectedIncr;
            ecMulti_line_cq_option.series[3].data=data.curedIncr;
            ecMulti_line_cq_option.series[4].data=data.deadIncr;
            ecMulti_line_cq.setOption(ecMulti_line_cq_option);
      },
       error:function(){
       }
   })
}
function get_cov_msg_data() {
    $.ajax({
        url: "/cov_msg",
        timeout: 10000,
        success: function (data) {
            $(".msg ul li").eq(0).text(data.msg1)
            $(".msg ul li").eq(1).text(data.msg2)
            $(".msg ul li").eq(2).text(data.msg3)
            $(".msg ul li").eq(3).text(data.msg4)
            $(".msg ul li").eq(4).text(data.msg5)
        },
        error: function () {
        }
    })
}

function get_covIncr_cq_data(){
   $.ajax({
       url:"/covIncr_cq",
       success:function (data){ //路由传来的数据data
            ecMulti_bar_option.xAxis.data = data.areaName;
            ecMulti_bar_option.series[0].data=data.localIncr;
            ecMulti_bar_option.series[1].data=data.asymptomaticIncr;
            ecMulti_bar_option.series[2].data=data.dangerArea;
            ecMulti_bar.setOption(ecMulti_bar_option);
      },
       error:function(){
       }
   })
}
get_top10_data()
get_wordcloud_data()
get_map_data()
get_total_data_of_china()
get_cov_trend_data()
get_cov_trend_cq_data()
get_cov_msg_data()
get_covIncr_cq_data()
