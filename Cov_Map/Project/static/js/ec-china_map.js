var echartsMap = echarts.init(document.getElementById('map_chart'));//, "dark");需下载dark主题

var myData = [{}];

var mapOption = {
    title: {
        text: '',//'现存确诊人数',
        subtext: '',
        left: 'center',

    },
    tooltip: {
        trigger: 'item'
    },
    //左侧导航图标
    visualMap: {
        show: true,
        x: 'left',
        y: 'bottom',
        textStyle: {
            fontSize: 8,
            color: '8A3310'
        },
        splitList: [
            { start: 0, end: 0 },
            { start: 1, end: 9 },
            { start: 10, end: 99 },
            { start: 100, end: 999 },
            {start:1000, end:9999},
            {start:10000}
        ],
        color: ['#8A3310', '#A60800', '#BF3730', '#E55B25', '#F2AD92', '#F9DCD1']
    },
    // 配置属性
    series: [{
        name: '现存确诊人数',//现存确诊人数',
        type: 'map',
        mapType: 'china',
        roam: false, //拖动和缩放
        itemStyle: {
            normal: {
                borderWidth: .5,
                borderColor: '#009FE8',
                areaColor: '#FFEFD5'
            },
            emphasis: { //鼠标滑过地图时高亮的设置
                borderWidth: .5,
                borderColor: '#4B0082',
                areaColor: '#FFF'
            }
        },
        label: {
            normal: {
                show: true,//省份名称
                fontSize: 8
            },
            emphasis: {
                show: true,
                fontSize: 8
            }
        },
        data: myData
    }]
};
echartsMap.setOption(mapOption)
