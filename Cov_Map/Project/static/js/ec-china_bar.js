var chartDom = document.getElementById('dynamic-bar');
var ecCov_top10 = echarts.init(chartDom);
var ecCov_top10_option;

// prettier-ignore
let dataAxis = [];// = ['点', '击', '柱', '子', '或', '者', '两', '指', '在', '触', '屏', '上', '滑'];
// prettier-ignore
let data = [];// = [220, 182, 191, 234, 290, 330, 310, 123, 442, 321, 90, 149, 210];
let yMax = 8000;
let dataShadow = [];
for (let i = 0; i < data.length; i++) {
  dataShadow.push(yMax);
}
ecCov_top10_option= {
  title: {
  },
  tooltip:{
      trigger:"axis",
      axisPointer:
      {
          type:"shadow"
      }
  },
  xAxis: {
    data: dataAxis,
    axisLabel: {
      inside: true,
      color: '#fff',
      fontSize:8
    },
    axisTick: {
      show: false
    },
    axisLine: {
      show: false
    },
    z: 20
  },
  yAxis: {
    axisLine: {
      show: false
    },
    axisTick: {
      show: true
    },
    axisLabel: {
      color: '#999'
    }
  },
  dataZoom: [
    {
      type: 'inside'
    }
  ],
  grid: [
    {
      show: false,
      z: 0,
      left: '0%',
      top: 10,
      right: '0%',
      bottom: 10,
      containLabel:true,
      backgroundColor: 'rgba(0,0,1,0)',
      borderWidth: 1,
      borderColor: '#ccc'
    }
  ],
  series: [
    {
      type: 'bar',
      showBackground: true,
      itemStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: '#83bff6' },
          { offset: 0.5, color: '#188df0' },
          { offset: 1, color: '#188df0' }
        ])
      },
      emphasis: {
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#2378f7' },
            { offset: 0.7, color: '#2378f7' },
            { offset: 1, color: '#83bff6' }
          ])
        }
      },
      data: data
    }
  ]
};
// Enable data zoom when user click bar.
const zoomSize = 6;
ecCov_top10.on('click', function (params) {
  console.log(dataAxis[Math.max(params.dataIndex - zoomSize / 2, 0)]);
  ecCov_top10.dispatchAction({
    type: 'dataZoom',
    startValue: dataAxis[Math.max(params.dataIndex - zoomSize / 2, 0)],
    endValue:
      dataAxis[Math.min(params.dataIndex + zoomSize / 2, data.length - 1)]
  });
});
ecCov_top10_option && ecCov_top10.setOption(ecCov_top10_option);
