var app = {};

var chartDom = document.getElementById('covIncr_cq');
var ecMulti_bar = echarts.init(chartDom);
var ecMulti_bar_option;

const posList = [
  'left',
  'right',
  'top',
  'bottom',
  'inside',
  'insideTop',
  'insideLeft',
  'insideRight',
  'insideBottom',
  'insideTopLeft',
  'insideTopRight',
  'insideBottomLeft',
  'insideBottomRight'
];
app.configParameters = {
  rotate: {
    min: -90,
    max: 90
  },
  align: {
    options: {
      left: 'left',
      center: 'center',
      right: 'right'
    }
  },
  verticalAlign: {
    options: {
      top: 'top',
      middle: 'middle',
      bottom: 'bottom'
    }
  },
  position: {
    options: posList.reduce(function (map, pos) {
      map[pos] = pos;
      return map;
    }, {})
  },
  distance: {
    min: 0,
    max: 100
  }
};
app.config = {
  rotate: 90,
  align: 'left',
  verticalAlign: 'middle',
  position: 'insideBottom',
  distance: 2,
  onChange: function () {
    const labelOption = {
      rotate: app.config.rotate,
      align: app.config.align,
      verticalAlign: app.config.verticalAlign,
      position: app.config.position,
      distance: app.config.distance
    };
    ecMulti_bar.setOption({
      series: [
        {
          label: labelOption
        },
        {
          label: labelOption
        },
        {
          label: labelOption
        },
        {
          label: labelOption
        }
      ]
    });
  }
};
const labelOption = {
  show: true,
  position: app.config.position,
  distance: app.config.distance,
  align: app.config.align,
  verticalAlign: app.config.verticalAlign,
  rotate: app.config.rotate,
  formatter: '{c}',
  fontSize: 8,
  rich: {
    name: {}
  }
};
ecMulti_bar_option = {
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'shadow'
    }
  },
  grid: [ //外围网格,因为预先留好了空隙,需重新设置外围网格与容器的空隙
    {
      show: false,
      z: 0,
      left: '0%',
      top: 7,
      right: '5%',
      bottom: 0,
      containLabel:true,
      backgroundColor: 'rgba(0,0,1,0)',
      borderWidth: 1,
      borderColor: '#ccc'
    }
  ],
  legend: {
    data: ['本土新增', '本土无症状', '风险地区']
  },
  toolbox: {
    show: true,
    orient: 'vertical',
    left: 'right',
    top: 'center',
    feature: {
      mark: { show: true },
      dataView: { show: true, readOnly: false },
      magicType: { show: true, type: ['line', 'bar', 'stack'] },
      restore: { show: true },
      saveAsImage: { show: true }
    }
  },
  xAxis: //注意要去掉外面的中括号
    {
      type: 'category',
      axisTick: { show: false },
      data: []
    },
  yAxis: [
    {
      type: 'value'
    }
  ],
  series: [
    {
      name: '本土新增',
      type: 'bar',
      barGap: 0,
      label: labelOption,
      emphasis: {
        focus: 'series'
      },
      data: []
    },
    {
      name: '本土无症状',
      type: 'bar',
      label: labelOption,
      emphasis: {
        focus: 'series'
      },
      data: []
    },
    {
      name: '风险地区',
      type: 'bar',
      label: labelOption,
      emphasis: {
        focus: 'series'
      },
      data: []
    },
  ]
};

ecMulti_bar_option && ecMulti_bar.setOption(ecMulti_bar_option);
