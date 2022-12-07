let ecWordCloud = echarts.init(document.getElementById('wordcloud'));

var data2 = []

var wordCloudOption = {
    tootip: {
        show: false
    },
    series: [{
        type: 'wordCloud',
        gridSize: 1,
        sizeRange: [10, 20],
        rotationRange: [-45, 0, 45, 90],
        textStyle: {
            color: function () { //新版echarts随机颜色设置不用写在normal中，否则可能会失效
                return 'rgb(' + [
                    Math.round(Math.random() * 255),
                    Math.round(Math.random() * 255),
                    Math.round(Math.random() * 255)
                ].join(',') + ')'
            },
            emphasis: {
                shadowBlur: 10,
                    shadowColor: '#333'
            }
        },
        width:'100%',
        height:'100%',
        right: null,
        bottom: null,
        data: data2
    }]
}

wordCloudOption && ecWordCloud.setOption(wordCloudOption);
