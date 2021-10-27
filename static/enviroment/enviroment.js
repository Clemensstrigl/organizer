var barData = {
  series: [
    {{projectedList}},
    {{actualList}}
  ]
};
var pieData = {
  labels: [
    {% if pieDataCompleted != 0 %}
    'completed'
    {% else %}
    '-'
    {% endif %}

    , {% if pieDataUnfinished != 0 %}
    'unfinished'
    {% else %}
    '-'
    {% endif %}],
  series: [{{pieDataCompleted}}, {{pieDataUnfinished}}]

};

var barOptions = {
  seriesBarDistance: 10,
  width: '400px',
  height: '400px',

};

var pieOptions = {
    width: '400px',
    height: '400px',
    chartPadding: 30,
    labelOffset: 100,
    labelDirection: 'explode'
};

var barResponsiveOptions = [
  ['screen and (max-width: 640px)', {
    seriesBarDistance: 5,
    axisX: {
      labelInterpolationFnc: function (value) {
        return value[0];
      }
    }
  }]
];

new Chartist.Bar('.barChart', barData, barOptions, barResponsiveOptions);

new Chartist.Pie('.pieChart', pieData, pieOptions);
